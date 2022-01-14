package cmd

import (
	"reflect"
	"testing"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

func TestGetClientNode(t *testing.T) {
	ts := time.Now().Unix()

	var cases = []struct {
		clients  map[string]*Client
		id       string
		expected *Node
	}{
		{map[string]*Client{"1": {Blockchain: "ethereum", LastCallTs: ts, Node: &Node{Alive: true}}}, "1", &Node{Alive: true}},
		{map[string]*Client{"2": {Blockchain: "polygon", LastCallTs: ts, Node: &Node{Alive: true}}}, "1", nil},
		{map[string]*Client{"1": {Blockchain: "ethereum", LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE, Node: &Node{Alive: true}}}, "1", nil},
	}
	for _, c := range cases {
		clientPool.Client = make(map[string]*Client)
		for id, client := range c.clients {
			clientPool.Client[id] = client
		}

		clientNode := clientPool.GetClientNode(c.id)
		if !reflect.DeepEqual(clientNode, c.expected) {
			t.Log("Wrong node returned")
			t.Fatal()
		}
	}
}

func TestCleanInactiveClientNodes(t *testing.T) {
	ts := time.Now().Unix()

	var cases = []struct {
		clients  map[string]*Client
		expected string
	}{
		{map[string]*Client{"1": {Blockchain: "ethereum", LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE}}, ""},
		{map[string]*Client{"1": {Blockchain: "ethereum", LastCallTs: ts}}, "1"},
		{map[string]*Client{
			"1": {Blockchain: "ethereum", LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE},
			"2": {Blockchain: "polygon", LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE - 10},
			"3": {Blockchain: "stellar", LastCallTs: ts},
		}, "3"},
	}
	for _, c := range cases {
		clientPool.Client = make(map[string]*Client)
		for id, client := range c.clients {
			clientPool.Client[id] = client
		}

		clientPool.CleanInactiveClientNodes()
		for key := range clientPool.Client {
			if key != c.expected {
				t.Log("Wrong client was removed")
				t.Fatal()
			}
		}
	}
}
