package cmd

import (
	"reflect"
	"testing"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

func TestAddClientNode(t *testing.T) {
	var cases = []struct {
		clients  map[string]*Client
		expected string
	}{
		{map[string]*Client{"1": {Node: &Node{Alive: true}}}, "1"},
	}
	for _, c := range cases {
		CreateClientPools()
		for id, client := range c.clients {
			ethereumClientPool.AddClientNode(id, client.Node)
		}
		for id := range ethereumClientPool.Client {
			if id != c.expected {
				t.Log("Wrong client was added")
				t.Fatal()
			}
		}
	}
}

func TestGetClientNode(t *testing.T) {
	ts := time.Now().Unix()

	var cases = []struct {
		clients  map[string]*Client
		id       string
		expected *Node
	}{
		{map[string]*Client{}, "1", nil},
		{map[string]*Client{"1": {LastCallTs: ts, Node: &Node{Alive: true}}}, "1", &Node{Alive: true}},
		{map[string]*Client{"2": {LastCallTs: ts, Node: &Node{Alive: true}}}, "1", nil},
		{map[string]*Client{"1": {LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE, Node: &Node{Alive: true}}}, "1", nil},
	}
	for _, c := range cases {
		CreateClientPools()
		for id, client := range c.clients {
			ethereumClientPool.Client[id] = client
		}

		clientNode := ethereumClientPool.GetClientNode(c.id)
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
		{map[string]*Client{"1": {LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE}}, ""},
		{map[string]*Client{"1": {LastCallTs: ts}}, "1"},
		{map[string]*Client{
			"1": {LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE},
			"2": {LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE - 10},
			"3": {LastCallTs: ts},
		}, "3"},
	}
	for _, c := range cases {
		CreateClientPools()
		for id, client := range c.clients {
			ethereumClientPool.Client[id] = client
		}

		ethereumClientPool.CleanInactiveClientNodes()
		for id := range ethereumClientPool.Client {
			if id != c.expected {
				t.Log("Wrong client was removed")
				t.Fatal()
			}
		}
	}
}
