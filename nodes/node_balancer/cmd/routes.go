/*
Handle routes for load balancer API.
*/
package cmd

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

// pingRoute response with status of load balancer server itself
func pingRoute(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

// lbHandler load balances the incoming requests to nodes
func lbHandler(w http.ResponseWriter, r *http.Request) {
	currentUserAccessRaw := r.Context().Value("currentUserAccess")
	currentUserAccess, ok := currentUserAccessRaw.(UserAccess)
	if !ok {
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	attempts := GetAttemptsFromContext(r)
	if attempts > configs.NB_CONNECTION_RETRIES {
		log.Printf("Max attempts reached from %s %s, terminating\n", r.RemoteAddr, r.URL.Path)
		http.Error(w, "Service not available", http.StatusServiceUnavailable)
		return
	}

	var blockchain string
	switch {
	case strings.HasPrefix(r.URL.Path, "/nb/ethereum"):
		blockchain = "ethereum"
	case strings.HasPrefix(r.URL.Path, "/nb/polygon"):
		blockchain = "polygon"
	default:
		http.Error(w, fmt.Sprintf("Unacceptable blockchain provided %s", blockchain), http.StatusBadRequest)
		return
	}

	// Chose one node
	var node *Node
	cpool, err := GetClientPool(blockchain)
	if err != nil {
		http.Error(w, fmt.Sprintf("Unacceptable blockchain provided %s", blockchain), http.StatusBadRequest)
		return
	}
	node = cpool.GetClientNode(currentUserAccess.AccessID)
	if node == nil {
		node = blockchainPool.GetNextNode(blockchain)
		if node == nil {
			http.Error(w, "There are no nodes available", http.StatusServiceUnavailable)
			return
		}
		cpool.AddClientNode(currentUserAccess.AccessID, node)
	}

	// Save origin path, to use in proxyErrorHandler if node will not response
	r.Header.Add("X-Origin-Path", r.URL.Path)

	switch {
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/ping", blockchain)):
		r.URL.Path = "/ping"
		node.StatusReverseProxy.ServeHTTP(w, r)
		return
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/jsonrpc", blockchain)):
		lbJSONRPCHandler(w, r, blockchain, node, currentUserAccess)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable path for %s blockchain %s", blockchain, r.URL.Path), http.StatusBadRequest)
		return
	}
}

func lbJSONRPCHandler(w http.ResponseWriter, r *http.Request, blockchain string, node *Node, currentUserAccess UserAccess) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Unable to read body", http.StatusBadRequest)
		return
	}
	r.Body = ioutil.NopCloser(bytes.NewBuffer(body))

	var jsonrpcRequest JSONRPCRequest
	err = json.Unmarshal(body, &jsonrpcRequest)
	if err != nil {
		http.Error(w, "Unable to parse JSON RPC request", http.StatusBadRequest)
		return
	}

	switch {
	case currentUserAccess.dataSource == "blockchain":
		if currentUserAccess.BlockchainAccess == false {
			http.Error(w, "Access to blockchain node not allowed with provided access id", http.StatusForbidden)
			return
		}
		if currentUserAccess.ExtendedMethods == false {
			err = verifyMethodWhitelisted(jsonrpcRequest.Method)
			if err != nil {
				http.Error(w, "Method for provided access id not allowed", http.StatusForbidden)
				return
			}
		}

		r.URL.Path = "/"
		node.GethReverseProxy.ServeHTTP(w, r)
		return
	case currentUserAccess.dataSource == "database":
		// lbDatabaseHandler(w, r, blockchain, jsonrpcRequest)
		http.Error(w, "Database access under development", http.StatusInternalServerError)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable data source %s", currentUserAccess.dataSource), http.StatusBadRequest)
		return
	}
}

func lbDatabaseHandler(w http.ResponseWriter, r *http.Request, blockchain string, jsonrpcRequest JSONRPCRequest) {
	switch {
	case jsonrpcRequest.Method == "eth_getBlockByNumber":
		var blockNumber uint64
		blockNumber, _ = strconv.ParseUint(jsonrpcRequest.Params[0].(string), 10, 32)

		block, err := databaseClient.GetBlock(blockchain, blockNumber)
		if err != nil {
			fmt.Printf("Unable to get block from database %v", err)
			http.Error(w, fmt.Sprintf("no such block %v", blockNumber), http.StatusBadRequest)
			return
		}
		fmt.Println(block)
	default:
		http.Error(w, fmt.Sprintf("Unsupported method %s by database, please use blockchain as data source", jsonrpcRequest.Method), http.StatusBadRequest)
		return
	}
}
