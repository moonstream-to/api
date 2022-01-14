/*
Handle routes for load balancer API.
*/
package cmd

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"strings"
)

// pingRoute response with status of load balancer server itself
func pingRoute(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

// lbHandler load balances the incoming requests to nodes
func lbHandler(w http.ResponseWriter, r *http.Request) {
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
	ip, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		http.Error(w, "Unable to parse client IP", http.StatusInternalServerError)
		return
	}

	var node *Node
	node = clientPool.GetClientNode(ip)
	if node == nil {
		node = blockchainPool.GetNextNode(blockchain)
		if node == nil {
			http.Error(w, "There are no nodes available", http.StatusServiceUnavailable)
			return
		}
		clientPool.AddClientNode(ip, blockchain, node)
	}

	// Save origin path, to use in proxyErrorHandler if node will not response
	r.Header.Add("X-Origin-Path", r.URL.Path)

	switch {
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/ping", blockchain)):
		r.URL.Path = "/ping"
		node.StatusReverseProxy.ServeHTTP(w, r)
		return
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/nb/%s/jsonrpc", blockchain)):
		r.URL.Path = "/"
		node.GethReverseProxy.ServeHTTP(w, r)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable path for %s blockchain %s", blockchain, r.URL.Path), http.StatusBadRequest)
		return
	}
}
