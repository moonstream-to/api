/*
Load balancer logic.
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
var blockchainPools map[string]*NodePool

// Node structure with
// Endpoint for geth/bor/etc node http.server endpoint
type Node struct {
	Endpoint *url.URL

	Alive        bool
	CurrentBlock uint64
	CallCounter  uint64

	mux sync.RWMutex

	GethReverseProxy *httputil.ReverseProxy
}

type TopNodeBlock struct {
	Block uint64
	Node  *Node
}

type NodePool struct {
	NodesMap map[string][]*Node
	NodesSet []*Node

	TopNode TopNodeBlock
}

// Node status response struct for HealthCheck
type NodeStatusResultResponse struct {
	Number string `json:"number"`
}

type NodeStatusResponse struct {
	Result NodeStatusResultResponse `json:"result"`
}

// AddNode to the nodes pool
func AddNode(blockchain string, tags []string, node *Node) {
	if blockchainPools == nil {
		blockchainPools = make(map[string]*NodePool)
	}
	if blockchainPools[blockchain] == nil {
		blockchainPools[blockchain] = &NodePool{}
	}
	if blockchainPools[blockchain].NodesMap == nil {
		blockchainPools[blockchain].NodesMap = make(map[string][]*Node)
	}
	blockchainPools[blockchain].NodesSet = append(blockchainPools[blockchain].NodesSet, node)

	for _, tag := range tags {
		blockchainPools[blockchain].NodesMap[tag] = append(
			blockchainPools[blockchain].NodesMap[tag],
			node,
		)
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

// FilterTagsNodes returns nodes with provided tags
func (npool *NodePool) FilterTagsNodes(tags []string) ([]*Node, TopNodeBlock) {
	nodesMap := npool.NodesMap
	nodesSet := npool.NodesSet

	tagSet := make(map[string]map[*Node]bool)

	for tag, nodes := range nodesMap {
		if tagSet[tag] == nil {
			tagSet[tag] = make(map[*Node]bool)
		}
		for _, node := range nodes {
			tagSet[tag][node] = true
		}
	}

	topNode := TopNodeBlock{}

	var filteredNodes []*Node
	for _, node := range nodesSet {
		accept := true
		for _, tag := range tags {
			if tagSet[tag][node] != true {
				accept = false
				break
			}
		}
		if accept {
			filteredNodes = append(filteredNodes, node)
			currentBlock := node.CurrentBlock
			if currentBlock >= npool.TopNode.Block {
				topNode.Block = currentBlock
				topNode.Node = node
			}
		}
	}

	return filteredNodes, topNode
}

// GetNextNode returns next active peer to take a connection
// Loop through entire nodes to find out an alive one and chose one with small CallCounter
func GetNextNode(nodes []*Node, topNode TopNodeBlock) *Node {
	nextNode := topNode.Node

	for _, node := range nodes {
		if node.IsAlive() {
			currentBlock := node.CurrentBlock
			if currentBlock < topNode.Block-NB_HIGHEST_BLOCK_SHIFT {
				// Bypass too outdated nodes
				continue
			}
			if node.CallCounter < nextNode.CallCounter {
				nextNode = node
			}
		}
	}

	if nextNode != nil {
		// Increase CallCounter value with 1
		atomic.AddUint64(&nextNode.CallCounter, uint64(1))
	}

	return nextNode
}

// SetNodeStatus modify status of the node
func SetNodeStatus(url *url.URL, alive bool) {
	for _, nodes := range blockchainPools {
		for _, n := range nodes.NodesSet {
			if n.Endpoint.String() == url.String() {
				n.SetAlive(alive)
				break
			}
		}
	}
}

// StatusLog logs node status
// TODO(kompotkot): Print list of alive and dead nodes
func StatusLog() {
	for blockchain, nodes := range blockchainPools {
		for _, n := range nodes.NodesSet {
			log.Printf(
				"Blockchain %s node %s is alive %t",
				blockchain, n.Endpoint.Host, n.Alive,
			)
		}
	}
}

// HealthCheck fetch the node latest block
func HealthCheck() {
	for blockchain, nodes := range blockchainPools {
		for _, node := range nodes.NodesSet {
			alive := false

			httpClient := http.Client{Timeout: NB_HEALTH_CHECK_CALL_TIMEOUT}
			resp, err := httpClient.Post(
				node.Endpoint.String(),
				"application/json",
				bytes.NewBuffer([]byte(`{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}`)),
			)
			if err != nil {
				node.UpdateNodeState(0, alive)
				log.Printf("Unable to reach node: %s", node.Endpoint.Host)
				continue
			}
			defer resp.Body.Close()

			body, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				node.UpdateNodeState(0, alive)
				log.Printf("Unable to parse response from %s node, err %v", node.Endpoint.Host, err)
				continue
			}

			var statusResponse NodeStatusResponse
			err = json.Unmarshal(body, &statusResponse)
			if err != nil {
				node.UpdateNodeState(0, alive)
				log.Printf("Unable to read json response from %s node, err: %v", node.Endpoint.Host, err)
				continue
			}

			blockNumberHex := strings.Replace(statusResponse.Result.Number, "0x", "", -1)
			blockNumber, err := strconv.ParseUint(blockNumberHex, 16, 64)
			if err != nil {
				node.UpdateNodeState(0, alive)
				log.Printf("Unable to parse block number from hex to string, err: %v", err)
				continue
			}

			// Mark node in list of pool as alive and update current block
			if blockNumber != 0 {
				alive = true
			}
			callCounter := node.UpdateNodeState(blockNumber, alive)

			if blockNumber > nodes.TopNode.Block {
				nodes.TopNode.Block = blockNumber
				nodes.TopNode.Node = node
			}

			if node.CallCounter >= NB_MAX_COUNTER_NUMBER {
				log.Printf(
					"Number of CallCounter for node %s reached %d limit, reset the counter.",
					node.Endpoint, NB_MAX_COUNTER_NUMBER,
				)
				atomic.StoreUint64(&node.CallCounter, uint64(0))
			}

			log.Printf(
				"Blockchain %s node %s is alive: %t with current block: %d called: %d times",
				blockchain, node.Endpoint.Host, alive, blockNumber, callCounter,
			)
		}
	}
}
