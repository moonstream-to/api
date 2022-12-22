/*
Handle routes for load balancer API.
*/
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"
)

type PingResponse struct {
	Status string `json:"status"`
}

// pingRoute response with status of load balancer server itself
func pingRoute(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

// lbHandler load balances the incoming requests to nodes
func lbHandler(w http.ResponseWriter, r *http.Request) {
	currentClientAccessRaw := r.Context().Value("currentClientAccess")
	currentClientAccess, ok := currentClientAccessRaw.(ClientResourceData)
	if !ok {
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	attempts := GetAttemptsFromContext(r)
	if attempts > NB_CONNECTION_RETRIES {
		log.Printf("Max attempts reached from %s %s, terminating", r.RemoteAddr, r.URL.Path)
		http.Error(w, "Service not available", http.StatusServiceUnavailable)
		return
	}

	var blockchain string
	for b := range configBlockchains {
		if strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/", b)) {
			blockchain = b
			break
		}
	}
	if blockchain == "" {
		http.Error(w, fmt.Sprintf("Unacceptable blockchain provided %s", blockchain), http.StatusBadRequest)
		return
	}

	// Save origin path, to use in proxyErrorHandler if node will not response
	r.Header.Add("X-Origin-Path", r.URL.Path)

	switch {
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/jsonrpc", blockchain)):
		lbJSONRPCHandler(w, r, blockchain, currentClientAccess)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable path for %s blockchain %s", blockchain, r.URL.Path), http.StatusBadRequest)
		return
	}
}

func lbJSONRPCHandler(w http.ResponseWriter, r *http.Request, blockchain string, currentClientAccess ClientResourceData) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Unable to read body", http.StatusBadRequest)
		return
	}
	r.Body = ioutil.NopCloser(bytes.NewBuffer(body))

	jsonrpcRequests, err := jsonrpcRequestParser(body)
	if err != nil {
		log.Println(err)
		http.Error(w, "Unable to parse JSON RPC request", http.StatusBadRequest)
		return
	}

	// Get tags from request params, sort and generate from it identifier
	var tags []string
	queries := r.URL.Query()
	for k, v := range queries {
		if k == "tag" {
			for _, tag := range v {
				tags = append(tags, tag)
			}
		}
	}

	// Chose one node
	var node *Node
	cpool := GetClientPool(blockchain)
	node = cpool.GetClientNode(currentClientAccess.AccessID)
	if node == nil {
		npool := blockchainPools[blockchain]
		var nodes []*Node
		var topNode TopNodeBlock
		if len(tags) != 0 {
			nodes, topNode = npool.FilterTagsNodes(tags)
		} else {
			topNode = npool.TopNode
			nodes = npool.NodesSet
		}
		node = GetNextNode(nodes, topNode)
		if node == nil {
			http.Error(w, "There are no nodes available", http.StatusServiceUnavailable)
			return
		}
		cpool.AddClientNode(currentClientAccess.AccessID, node)
	}

	switch {
	case currentClientAccess.dataSource == "blockchain":
		if currentClientAccess.BlockchainAccess == false {
			http.Error(w, "Access to blockchain node not allowed with provided access id", http.StatusForbidden)
			return
		}
		if currentClientAccess.ExtendedMethods == false {
			for _, jsonrpcRequest := range jsonrpcRequests {
				_, exists := ALLOWED_METHODS[jsonrpcRequest.Method]
				if !exists {
					http.Error(w, "Method for provided access id not allowed", http.StatusForbidden)
					return
				}
			}
		}

		// Overwrite Path so response will be returned to correct place
		r.URL.Path = "/"
		node.GethReverseProxy.ServeHTTP(w, r)
		return
	case currentClientAccess.dataSource == "database":
		// lbDatabaseHandler(w, r, blockchain, jsonrpcRequest)
		http.Error(w, "Database access under development", http.StatusInternalServerError)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable data source %s", currentClientAccess.dataSource), http.StatusBadRequest)
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
			log.Printf("Unable to get block from database, err: %v", err)
			http.Error(w, fmt.Sprintf("no such block %v", blockNumber), http.StatusBadRequest)
			return
		}
		fmt.Println(block)
	default:
		http.Error(w, fmt.Sprintf("Unsupported method %s by database, please use blockchain as data source", jsonrpcRequest.Method), http.StatusBadRequest)
		return
	}
}
