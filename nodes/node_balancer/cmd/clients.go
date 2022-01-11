package cmd

import (
	"log"
	"reflect"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var clientPool ClientPool

// Add client node and client itself if doesn't exist
// TODO(kompotkot): Add mutes as for balancer
func (cpool *ClientPool) AddClientNode(ip, blockchain string, node *Node) {
	ts := time.Now().Unix()

	// Find in list clint with same IP
	var client *Client
	for _, c := range cpool.Clients {
		if c.IP == ip {
			client = c
		}
	}

	// Add new client if doesn't exist
	if client == nil {
		client = &Client{
			IP: ip,
		}
		cpool.Clients = append(cpool.Clients, client)
	}

	newNode := true
	for _, cn := range client.ClientNodes {
		if reflect.DeepEqual(cn.Node, node) {
			cn.LastCallTs = ts
			newNode = false
		}
	}

	if newNode {
		client.ClientNodes = append(client.ClientNodes, ClientNode{
			Blockchain: blockchain,
			Node:       node,
			LastCallTs: ts,
		})
	}
}

// Get client hot node if exists
// TODO(kompotkot): Add mutes as for balancer
func (cpool *ClientPool) GetClientNode(blockchain, ip string) *Node {
	ts := time.Now().Unix()

	for _, c := range cpool.Clients {
		if c.IP == ip {
			for j, cn := range c.ClientNodes {
				if cn.Blockchain == blockchain {
					if ts-cn.LastCallTs < configs.NB_CLIENT_NODE_KEEP_ALIVE {
						// Hot node for client found, use it
						if cn.Node.IsAlive() {
							cn.LastCallTs = ts
							return cn.Node
						}
					}
					// Remove outdated hot node from client hot nodes list
					c.ClientNodes = append(c.ClientNodes[:j], c.ClientNodes[j+1:]...)
				}
			}
		}
	}

	return nil
}

// Clean client list of hot nodes from outdated
// TODO(kompotkot): Add mutes as for balancer
func (cpool *ClientPool) CleanInactiveClientNodes() {
	ts := time.Now().Unix()

	for i, c := range cpool.Clients {
		for j, cn := range c.ClientNodes {
			if ts-cn.LastCallTs >= configs.NB_CLIENT_NODE_KEEP_ALIVE {
				// Remove client's node
				c.ClientNodes = append(c.ClientNodes[:j], c.ClientNodes[j+1:]...)
			}
		}

		// If there are no hot nodes under client, remove client
		if len(c.ClientNodes) == 0 {
			cpool.Clients = append(cpool.Clients[:i], cpool.Clients[i+1:]...)
		}
	}

	log.Printf("Active clients: %d\n", len(cpool.Clients))
}
