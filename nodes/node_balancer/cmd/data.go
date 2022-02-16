/*
Data structure.
*/
package cmd

import (
	"net/http/httputil"
	"net/url"
	"sync"
)

type PingResponse struct {
	Status string `json:"status"`
}

type NodeStatusResponse struct {
	CurrentBlock uint64 `json:"current_block"`
}

// Node - which one node client worked with
// LastCallTs - timestamp from last call
type Client struct {
	Node       *Node
	LastCallTs int64

	mux sync.RWMutex
}

type ClientPool struct {
	Client map[string]*Client
}

// Node structure with
// StatusURL for status server at node endpoint
// GethURL for geth/bor/etc node http.server endpoint
type Node struct {
	StatusURL *url.URL
	GethURL   *url.URL

	Alive        bool
	CurrentBlock uint64

	mux sync.RWMutex

	StatusReverseProxy *httputil.ReverseProxy
	GethReverseProxy   *httputil.ReverseProxy
}

type NodePool struct {
	Blockchain string
	Nodes      []*Node

	// Counter to observe all nodes
	Current uint64
}

type BlockchainPool struct {
	Blockchains []*NodePool
}
