package main

import (
	"reflect"
	"testing"
	"time"
)

// TestAddClientNode tests adding new client to client pool
func TestAddClientNode(t *testing.T) {
	var cases = []struct {
		clients  map[string]*Client
		expected string
	}{
		{map[string]*Client{"1": {Node: &Node{Alive: true}}}, "1"},
	}

	for _, c := range cases {
		CreateClientPools()
		cpool := GetClientPool("ethereum")

		for id, client := range c.clients {
			cpool.AddClientNode(id, client.Node)
		}
		for id := range cpool.Client {
			if id != c.expected {
				t.Log("Wrong client was added")
				t.Fatal()
			}
		}
	}
}

// TestGetClientNode tests getting correct client
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
	}

	for _, c := range cases {
		CreateClientPools()
		cpool := GetClientPool("ethereum")

		for id, client := range c.clients {
			cpool.AddClientNode(id, client.Node)
		}

		clientNode := cpool.GetClientNode(c.id)
		if !reflect.DeepEqual(clientNode, c.expected) {
			t.Log("Wrong node returned")
			t.Fatal()
		}
	}
}

// TestCleanInactiveClientNodes tests cleaning inactive clients
func TestCleanInactiveClientNodes(t *testing.T) {
	ts := time.Now().Unix()

	var cases = []struct {
		clients  map[string]*Client
		expected string
	}{
		{map[string]*Client{"1": {LastCallTs: ts - NB_CLIENT_NODE_KEEP_ALIVE}}, ""},
		{map[string]*Client{"1": {LastCallTs: ts}}, "1"},
		{map[string]*Client{
			"1": {LastCallTs: ts - NB_CLIENT_NODE_KEEP_ALIVE},
			"2": {LastCallTs: ts - NB_CLIENT_NODE_KEEP_ALIVE - 10},
			"3": {LastCallTs: ts},
		}, "3"},
	}
	for _, c := range cases {
		CreateClientPools()
		cpool := GetClientPool("ethereum")

		for id, client := range c.clients {
			cpool.Client[id] = client
		}

		cpool.CleanInactiveClientNodes()
		for id := range cpool.Client {
			if id != c.expected {
				t.Log("Wrong client was removed")
				t.Fatal()
			}
		}
	}
}
