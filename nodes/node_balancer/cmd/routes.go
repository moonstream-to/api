/*
Handle routes for load balancer API.
*/
package cmd

import (
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
	userRaw := r.Context().Value("user")
	user, ok := userRaw.(BugoutUserResponse)
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
	node = cpool.GetClientNode(user.ID)
	if node == nil {
		node = blockchainPool.GetNextNode(blockchain)
		if node == nil {
			http.Error(w, "There are no nodes available", http.StatusServiceUnavailable)
			return
		}
		cpool.AddClientNode(user.ID, node)
	}

	// Save origin path, to use in proxyErrorHandler if node will not response
	r.Header.Add("X-Origin-Path", r.URL.Path)

	switch {
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/ping", blockchain)):
		r.URL.Path = "/ping"
		node.StatusReverseProxy.ServeHTTP(w, r)
		return
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/jsonrpc", blockchain)):
		lbJSONRPCHandler(w, r, blockchain, node, user)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable path for %s blockchain %s", blockchain, r.URL.Path), http.StatusBadRequest)
		return
	}
}

func lbJSONRPCHandler(w http.ResponseWriter, r *http.Request, blockchain string, node *Node, user BugoutUserResponse) {
	var dataSource string
	dataSources := r.Header[configs.MOONSTREAM_DATA_SOURCE_HEADER]
	// TODO(kompotkot): Re-write it, to be able to work without database
	if len(dataSources) == 0 {
		dataSource = "database"
	} else {
		dataSource = dataSources[0]
	}

	switch {
	case dataSource == "blockchain":
		if user.ID != controllerUserID {
			resources, err := bugoutClient.GetResources(configs.BUGOUT_NODE_BALANCER_CONTROLLER_TOKEN, user.ID)
			if err != nil {
				http.Error(w, fmt.Sprintf("not allowed %s", dataSource), http.StatusBadRequest)
				return
			}

			blockchainAccess := false
			for _, resource := range resources.Resources {
				if resource.ResourceData.BlockchainAccess == true {
					blockchainAccess = true
				}
			}

			if blockchainAccess == false {
				http.Error(w, fmt.Sprintf("not allowed %s", dataSource), http.StatusBadRequest)
				return
			}
		}

		fmt.Println("proxied to node")
		// r.URL.Path = "/"
		// node.GethReverseProxy.ServeHTTP(w, r)
		return
	case dataSource == "database":
		lbDatabaseHandler(w, r, blockchain)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable data source %s", dataSource), http.StatusBadRequest)
		return
	}
}

type JSONRPCRequest struct {
	Jsonrpc string        `json:"jsonrpc"`
	Method  string        `json:"method"`
	Params  []interface{} `json:"params"`
	ID      uint64        `json:"id"`
}

// var ALLOWED_ETH_ENDPOINTS = []string{"eth_getBlockByNumber"}

func lbDatabaseHandler(w http.ResponseWriter, r *http.Request, blockchain string) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Println(err)
		return
	}
	var jsonrpcRequest JSONRPCRequest
	err = json.Unmarshal(body, &jsonrpcRequest)
	if err != nil {
		fmt.Println(err)
		return
	}

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
