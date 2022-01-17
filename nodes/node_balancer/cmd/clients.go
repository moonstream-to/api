package cmd

import (
	"errors"
	"reflect"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var ethereumClientPool ClientPool
var polygonClientPool ClientPool

// Generate client pools for different blockchains
func CreateClientPools() {
	ethereumClientPool.Client = make(map[string]*Client)
	polygonClientPool.Client = make(map[string]*Client)
}

// Return client pool correspongin to blockchain
func GetClientPool(blockchain string) (*ClientPool, error) {
	var cpool *ClientPool
	if blockchain == "ethereum" {
		cpool = &ethereumClientPool
	} else if blockchain == "polygon" {
		cpool = &polygonClientPool
	} else {
		return nil, errors.New("Unexisting blockchain provided")
	}
	return cpool, nil
}

// Updates client last appeal to node
func (client *Client) UpdateClientLastCall() {
	ts := time.Now().Unix()

	client.mux.Lock()
	client.LastCallTs = ts
	client.mux.Unlock()
}

// Get number of seconds from current last call to client node
func (client *Client) GetClientLastCallDiff() (lastCallTs int64) {
	ts := time.Now().Unix()

	client.mux.RLock()
	lastCallTs = ts - client.LastCallTs
	client.mux.RUnlock()

	return lastCallTs
}

// Find clint with same ID and update timestamp or
// add new one if doesn't exist
func (cpool *ClientPool) AddClientNode(id string, node *Node) {

	if cpool.Client[id] != nil {
		if reflect.DeepEqual(cpool.Client[id].Node, node) {
			cpool.Client[id].UpdateClientLastCall()
			return
		}
	}
	cpool.Client[id] = &Client{
		Node:       node,
		LastCallTs: time.Now().Unix(),
	}
}

// Get client hot node if exists
func (cpool *ClientPool) GetClientNode(id string) *Node {
	if cpool.Client[id] != nil {
		lastCallTs := cpool.Client[id].GetClientLastCallDiff()
		if lastCallTs < configs.NB_CLIENT_NODE_KEEP_ALIVE {
			cpool.Client[id].UpdateClientLastCall()
			return cpool.Client[id].Node
		}
		delete(cpool.Client, id)
	}

	return nil
}

// Clean client list of hot outdated nodes
func (cpool *ClientPool) CleanInactiveClientNodes() int {
	cnt := 0
	for id, client := range cpool.Client {
		lastCallTs := client.GetClientLastCallDiff()
		if lastCallTs >= configs.NB_CLIENT_NODE_KEEP_ALIVE {
			delete(cpool.Client, id)
		} else {
			cnt += 1
		}
	}

	return cnt
}
