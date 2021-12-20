/*
Handle routes for load balancer API.
*/
package cmd

import (
	"encoding/json"
	"fmt"
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
	case strings.HasPrefix(r.URL.Path, "/lb/ethereum"):
		blockchain = "ethereum"
	case strings.HasPrefix(r.URL.Path, "/lb/polygon"):
		blockchain = "polygon"
	default:
		http.Error(w, fmt.Sprintf("Unacceptable blockchain provided %s", blockchain), http.StatusBadRequest)
		return
	}

	// Chose one node
	peer := blockchainPool.GetNextPeer(blockchain)
	if peer == nil {
		http.Error(w, "There are no nodes available", http.StatusServiceUnavailable)
		return
	}

	// Save origin path, to use in proxyErrorHandler if node will not response
	r.Header.Add("X-Origin-Path", r.URL.Path)

	switch {
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/lb/%s/ping", blockchain)):
		r.URL.Path = "/ping"
		peer.StatusReverseProxy.ServeHTTP(w, r)
		return
	case strings.HasPrefix(r.URL.Path, fmt.Sprintf("/lb/%s/rpc", blockchain)):
		r.URL.Path = "/"
		peer.GethReverseProxy.ServeHTTP(w, r)
		return
	default:
		http.Error(w, fmt.Sprintf("Unacceptable path for %s blockchain %s", blockchain, r.URL.Path), http.StatusBadRequest)
		return
	}
}
