package main

import (
	"reflect"
	"testing"
	"time"
)

func clientsSetupSuit(t *testing.T) func(t *testing.T) {
	t.Log("Setup suit")

	supportedBlockchains = map[string]bool{"ethereum": true}

	return func(t *testing.T) {
		t.Log("Teardown suit")
	}
}

func TestAddClientNode(t *testing.T) {
	teardownSuit := clientsSetupSuit(t)
	defer teardownSuit(t)

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

func TestGetClientNode(t *testing.T) {
	teardownSuit := clientsSetupSuit(t)
	defer teardownSuit(t)

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

func TestCleanInactiveClientNodes(t *testing.T) {
	teardownSuit := clientsSetupSuit(t)
	defer teardownSuit(t)

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
