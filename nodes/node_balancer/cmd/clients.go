package cmd

import (
	"log"
	"reflect"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var clientPool ClientPool

// func (client *Client) GetClientNode() (clientNode *Node) {
// 	client.mux.RLock()
// 	clientNode = client.Node
// 	client.mux.RUnlock()
// 	return clientNode
// }

// Add client node and client itself if doesn't exist
// TODO(kompotkot): Add mutex as for balancer
func (cpool *ClientPool) AddClientNode(id, blockchain string, node *Node) {
	ts := time.Now().Unix()

	// Find clint with same ID and update timestamp or
	// add new one if doesn't exist
	if cpool.Client[id] != nil {
		if reflect.DeepEqual(cpool.Client[id].Node, node) {
			cpool.Client[id].LastCallTs = ts
			return
		}
	}
	cpool.Client[id] = &Client{
		Blockchain: blockchain,
		Node:       node,
		LastCallTs: ts,
	}
}

// Get client hot node if exists
// TODO(kompotkot): Add mutex as for balancer
func (cpool *ClientPool) GetClientNode(id string) *Node {
	ts := time.Now().Unix()

	currentClient := cpool.Client[id]

	if currentClient != nil {
		if ts-currentClient.LastCallTs < configs.NB_CLIENT_NODE_KEEP_ALIVE {
			currentClient.LastCallTs = ts
			return currentClient.Node
		}
		delete(cpool.Client, id)
	}

	return nil
}

// Clean client list of hot nodes from outdated
// TODO(kompotkot): Add mutex as for balancer
func (cpool *ClientPool) CleanInactiveClientNodes() {
	ts := time.Now().Unix()

	cnt := 0
	for id, client := range cpool.Client {
		if ts-client.LastCallTs >= configs.NB_CLIENT_NODE_KEEP_ALIVE {
			delete(cpool.Client, id)
		} else {
			cnt += 1
		}
	}

	log.Printf("Active clients: %d\n", cnt)
}
