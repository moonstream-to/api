package cmd

import (
	"fmt"
	"log"
	"reflect"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var clientPool ClientPool

func (cpool *ClientPool) AddClient(ip string) {
	var client *Client
	for _, c := range cpool.Clients {
		if c.IP == ip {
			client = c
		}
	}

	if client == nil {
		fmt.Println("Adding new client")
		client = &Client{
			IP: ip,
		}
		cpool.Clients = append(cpool.Clients, client)
	}
}

func (cpool *ClientPool) AddClientNode(ip, blockchain string, node *Node) {
	ts := time.Now().Unix()

	for _, c := range cpool.Clients {
		if c.IP == ip {
			newNode := true

			for _, cn := range c.ClientNodes {
				if reflect.DeepEqual(cn.Node, node) {
					cn.LastCallTs = ts
					newNode = false
				}
			}

			if newNode {
				c.ClientNodes = append(c.ClientNodes, ClientNode{
					Blockchain: blockchain,
					Node:       node,
					LastCallTs: ts,
				})
			}
		}
	}
}

func (cpool *ClientPool) GetClientNode(blockchain, ip string) *Node {
	ts := time.Now().Unix()

	for _, c := range cpool.Clients {
		if c.IP == ip {
			for j, cn := range c.ClientNodes {
				if cn.Blockchain == blockchain {
					if ts-cn.LastCallTs < configs.NB_CLIENT_NODE_KEEP_ALIVE {
						cn.LastCallTs = ts
						fmt.Println("Hot client node found, re-use it")
						return cn.Node
					} else {
						fmt.Println("Client node outdated, remove it")
						c.ClientNodes = append(c.ClientNodes[:j], c.ClientNodes[j+1:]...)
					}
				}
			}
		}
	}

	return nil
}

func (cpool *ClientPool) CleanInactiveClientNodes() {
	ts := time.Now().Unix()

	for i, c := range cpool.Clients {
		for j, cn := range c.ClientNodes {
			if ts-cn.LastCallTs >= configs.NB_CLIENT_NODE_KEEP_ALIVE {
				fmt.Println("Removing client node")
				c.ClientNodes = append(c.ClientNodes[:j], c.ClientNodes[j+1:]...)
			}
		}
		if len(c.ClientNodes) == 0 {
			fmt.Println("Removing client itself")
			cpool.Clients = append(cpool.Clients[:i], cpool.Clients[i+1:]...)
		}
	}
}
func (cpool *ClientPool) StatusLog() {
	log.Printf("Active clients: %d", len(cpool.Clients))
}
