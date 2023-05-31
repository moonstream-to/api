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
	CallCounter  uint64

	mux sync.RWMutex

	GethReverseProxy *httputil.ReverseProxy
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

// UpdateNodeState updates block number and live status,
// also it returns number of time node appeal
func (node *Node) UpdateNodeState(currentBlock uint64, alive bool) (callCounter uint64) {
	node.mux.Lock()
	node.CurrentBlock = currentBlock
	node.Alive = alive

	callCounter = node.CallCounter
	node.mux.Unlock()
	return callCounter
}

// IncreaseCallCounter increased to 1 each time node called
func (node *Node) IncreaseCallCounter() {
	node.mux.Lock()
	if node.CallCounter >= NB_MAX_COUNTER_NUMBER {
		log.Printf("Number of calls for node %s reached %d limit, reset the counter.", node.Endpoint, NB_MAX_COUNTER_NUMBER)
		node.CallCounter = uint64(0)
	} else {
		node.CallCounter++
	}
	node.mux.Unlock()
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

	// Increase Current value with 1
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
			alive := false

			httpClient := http.Client{Timeout: NB_HEALTH_CHECK_CALL_TIMEOUT}
			resp, err := httpClient.Post(
				n.Endpoint.String(),
				"application/json",
				bytes.NewBuffer([]byte(`{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}`)),
			)
			if err != nil {
				n.UpdateNodeState(0, alive)
				log.Printf("Unable to reach node: %s", n.Endpoint.Host)
				if resp != nil {
					resp.Body.Close()
				}
				continue
			}

			body, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				n.UpdateNodeState(0, alive)
				log.Printf("Unable to parse response from %s node, err %v", n.Endpoint.Host, err)
				if resp.Body != nil {
					resp.Body.Close()
				}
				continue
			}
			resp.Body.Close()

			var statusResponse NodeStatusResponse
			err = json.Unmarshal(body, &statusResponse)
			if err != nil {
				n.UpdateNodeState(0, alive)
				log.Printf("Unable to read json response from %s node, err: %v", n.Endpoint.Host, err)
				continue
			}

			blockNumberHex := strings.Replace(statusResponse.Result.Number, "0x", "", -1)
			blockNumber, err := strconv.ParseUint(blockNumberHex, 16, 64)
			if err != nil {
				n.UpdateNodeState(0, alive)
				log.Printf("Unable to parse block number from hex to string, err: %v", err)
				continue
			}

			// Mark node in list of pool as alive and update current block
			if blockNumber != 0 {
				alive = true
			}
			callCounter := n.UpdateNodeState(blockNumber, alive)

			log.Printf(
				"Node %s is alive: %t with current block: %d called: %d times", n.Endpoint.Host, alive, blockNumber, callCounter,
			)
		}
	}
}
