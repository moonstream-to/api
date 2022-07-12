/*
Load balancer, based on https://github.com/kasvith/simplelb/
*/
package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
)

// Main variable of pool of blockchains which contains pool of nodes
// for each blockchain we work during session.
var blockchainPool BlockchainPool

// Node structure with
// StatusURL for status server at node endpoint
// Endpoint for geth/bor/etc node http.server endpoint
type Node struct {
	Endpoint *url.URL

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

// Node status response struct for HealthCheck
type NodeStatusResultResponse struct {
	Number string `json:"number"`
}

type NodeStatusResponse struct {
	Result NodeStatusResultResponse `json:"result"`
}

// AddNode to the nodes pool
func (bpool *BlockchainPool) AddNode(node *Node, blockchain string) {
	var nodePool *NodePool
	for _, b := range bpool.Blockchains {
		if b.Blockchain == blockchain {
			nodePool = b
		}
	}

	// Check if blockchain not yet in pool
	if nodePool == nil {
		nodePool = &NodePool{
			Blockchain: blockchain,
		}
		nodePool.Nodes = append(nodePool.Nodes, node)
		bpool.Blockchains = append(bpool.Blockchains, nodePool)
	} else {
		nodePool.Nodes = append(nodePool.Nodes, node)
	}
}

// SetAlive with mutex for exact node
func (node *Node) SetAlive(alive bool) {
	node.mux.Lock()
	node.Alive = alive
	node.mux.Unlock()
}

// IsAlive returns true when node is alive
func (node *Node) IsAlive() (alive bool) {
	node.mux.RLock()
	alive = node.Alive
	node.mux.RUnlock()
	return alive
}

// SetCurrentBlock with mutex for exact node
func (node *Node) SetCurrentBlock(currentBlock uint64) {
	node.mux.Lock()
	node.CurrentBlock = currentBlock
	node.mux.Unlock()
}

// GetCurrentBlock returns block number
func (node *Node) GetCurrentBlock() (currentBlock uint64) {
	node.mux.RLock()
	currentBlock = node.CurrentBlock
	node.mux.RUnlock()
	return currentBlock
}

// GetNextNode returns next active peer to take a connection
// Loop through entire nodes to find out an alive one
func (bpool *BlockchainPool) GetNextNode(blockchain string) *Node {
	highestBlock := uint64(0)

	// Get NodePool with correct blockchain
	var np *NodePool
	for _, b := range bpool.Blockchains {
		if b.Blockchain == blockchain {
			np = b
			for _, n := range b.Nodes {
				if n.CurrentBlock > highestBlock {
					highestBlock = n.CurrentBlock
				}
			}
		}
	}

	// Increase Current value with 1 to be able to track node appeals
	currentInc := atomic.AddUint64(&np.Current, uint64(1))

	// next is an Atomic incrementer, value always in range from 0 to slice length,
	// it returns an index of slice
	next := int(currentInc % uint64(len(np.Nodes)))

	// Start from next one and move full cycle
	l := len(np.Nodes) + next

	for i := next; i < l; i++ {
		// Take an index by modding with length
		idx := i % len(np.Nodes)
		// If we have an alive one, use it and store if its not the original one
		if np.Nodes[idx].IsAlive() {
			if i != next {
				// Mark the current one
				atomic.StoreUint64(&np.Current, uint64(idx))
			}
			// Pass nodes with low blocks
			// TODO(kompotkot): Re-write to not rotate through not highest blocks
			if np.Nodes[idx].CurrentBlock < highestBlock {
				continue
			}

			return np.Nodes[idx]
		}
	}
	return nil
}

// SetNodeStatus modify status of the node
func (bpool *BlockchainPool) SetNodeStatus(url *url.URL, alive bool) {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			if n.Endpoint.String() == url.String() {
				n.SetAlive(alive)
				break
			}
		}
	}
}

// StatusLog logs node status
// TODO(kompotkot): Print list of alive and dead nodes
func (bpool *BlockchainPool) StatusLog() {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			log.Printf(
				"Blockchain %s node %s is alive %t. Blockchain called %d times",
				b.Blockchain, n.Endpoint.Host, n.Alive, b.Current,
			)
		}
	}
}

// HealthCheck fetch the node latest block
func (bpool *BlockchainPool) HealthCheck() {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			httpClient := http.Client{Timeout: NB_HEALTH_CHECK_CALL_TIMEOUT}
			resp, err := httpClient.Post(
				n.Endpoint.String(),
				"application/json",
				bytes.NewBuffer([]byte(`{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}`)),
			)
			if err != nil {
				n.SetAlive(false)
				n.SetCurrentBlock(0)
				log.Printf("Unable to reach node: %s", n.Endpoint.Host)
				continue
			}
			defer resp.Body.Close()

			body, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				n.SetAlive(false)
				n.SetCurrentBlock(0)
				log.Printf("Unable to parse response from %s node, err %v", n.Endpoint.Host, err)
				continue
			}

			var statusResponse NodeStatusResponse
			err = json.Unmarshal(body, &statusResponse)
			if err != nil {
				n.SetAlive(false)
				n.SetCurrentBlock(0)
				log.Printf("Unable to read json response from %s node, err: %v", n.Endpoint.Host, err)
				continue
			}

			blockNumberHex := strings.Replace(statusResponse.Result.Number, "0x", "", -1)
			blockNumber, err := strconv.ParseUint(blockNumberHex, 16, 64)
			if err != nil {
				n.SetAlive(false)
				n.SetCurrentBlock(0)
				log.Printf("Unable to parse block number from hex to string, err: %v", err)
				continue
			}

			// Mark node in list of nodes as alive or not and update current block
			var alive bool
			if blockNumber != 0 {
				alive = true
			} else {
				alive = false
			}
			n.SetAlive(alive)
			n.SetCurrentBlock(blockNumber)

			log.Printf(
				"Node %s is alive: %t with current block: %d blockchain called: %d times",
				n.Endpoint.Host, alive, blockNumber, b.Current,
			)
		}
	}
}
