/*
Load balancer, based on https://github.com/kasvith/simplelb/
*/
package cmd

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"sync/atomic"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

// Main variable of pool of blockchains which contains pool of nodes
// for each blockchain we work during session.
var blockchainPool BlockchainPool

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

// SetNodeStatus changes a status of a node by StatusURL or GethURL
func (bpool *BlockchainPool) SetNodeStatus(url *url.URL, alive bool) {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			if n.StatusURL.String() == url.String() || n.GethURL.String() == url.String() {
				n.SetAlive(alive)
				break
			}
		}
	}
}

// StatusLog logs nodes statuses
// TODO(kompotkot): Print list of alive and dead nodes
func (bpool *BlockchainPool) StatusLog() {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			log.Printf(
				"Blockchain %s node %s is alive %t. Blockchain called %d times",
				b.Blockchain, n.StatusURL, n.Alive, b.Current,
			)
		}
	}
}

// HealthCheck fetch the node status and current block server
func (bpool *BlockchainPool) HealthCheck() {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			n.SetAlive(false)
			n.SetCurrentBlock(0)

			// Get response from node /ping endpoint
			httpClient := http.Client{Timeout: configs.NB_HEALTH_CHECK_CALL_TIMEOUT}
			resp, err := httpClient.Get(fmt.Sprintf("%s/status", n.StatusURL))
			if err != nil {
				log.Printf("Unable to reach node: %s\n", n.StatusURL)
				continue
			}
			defer resp.Body.Close()

			body, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				log.Printf("Unable to parse response from node: %s\n", n.StatusURL)
				continue
			}

			var statusResponse NodeStatusResponse
			err = json.Unmarshal(body, &statusResponse)
			if err != nil {
				log.Printf("Unable to read json response from node: %s\n", n.StatusURL)
				continue
			}

			// Mark node in list of nodes as alive or not and update current block
			n.SetAlive(true)
			if statusResponse.CurrentBlock != 0 {
				n.SetCurrentBlock(statusResponse.CurrentBlock)
			}

			log.Printf("Node %s is alive: %t with current block: %d blockchain called: %d times\n", n.StatusURL, true, statusResponse.CurrentBlock, b.Current)
		}
	}
}
