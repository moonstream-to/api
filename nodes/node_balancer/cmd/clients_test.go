package cmd

import (
	"reflect"
	"testing"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

func TestAddClient(t *testing.T) {
	var cases = []struct {
		clients  []Client
		ip       string
		expected int
	}{
		{[]Client{}, "localhost", 1},
		{[]Client{{IP: "localhost"}}, "192.168.1.2", 2},
	}
	for _, c := range cases {
		clientPool.Clients = []*Client{}
		for _, client := range c.clients {
			clientPool.Clients = append(clientPool.Clients, &client)
		}

		clientPool.AddClient(c.ip)
		if len(clientPool.Clients) != c.expected {
			t.Log("Wrong number of clients")
			t.Fatal()
		}
	}
}

func TestCleanInactiveClientNodes(t *testing.T) {
	ts := time.Now().Unix()

	var cases = []struct {
		clients  []Client
		expected int
	}{
		{[]Client{{IP: "localhost", ClientNodes: []ClientNode{{LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE}}}}, 0},
		{[]Client{{IP: "localhost", ClientNodes: []ClientNode{{LastCallTs: ts}}}}, 1},
		{[]Client{
			{IP: "localhost", ClientNodes: []ClientNode{
				{LastCallTs: ts, Blockchain: "polygon"},
				{LastCallTs: ts, Blockchain: "ethereum"},
				{LastCallTs: ts - configs.NB_CLIENT_NODE_KEEP_ALIVE - 1, Blockchain: "solana"},
			}}}, 2},
	}
	for _, c := range cases {
		clientPool.Clients = []*Client{}
		for _, client := range c.clients {
			clientPool.Clients = append(clientPool.Clients, &client)
		}

		clientPool.CleanInactiveClientNodes()
		for _, client := range clientPool.Clients {
			if len(client.ClientNodes) != c.expected {
				t.Log("Wrong number of client nodes")
				t.Fatal()
			}
		}

	}
}

func TestGetClientNode(t *testing.T) {
	var cases = []struct {
		clients    []Client
		blockchain string
		ip         string
		expected   *Node
	}{
		{[]Client{{IP: "localhost"}}, "ethereum", "192.168.1.2", nil},
	}
	for _, c := range cases {
		clientPool.Clients = []*Client{}
		for _, client := range c.clients {
			clientPool.Clients = append(clientPool.Clients, &client)
		}

		clientNode := clientPool.GetClientNode(c.blockchain, c.ip)
		if !reflect.DeepEqual(clientNode, c.expected) {
			t.Log("Wrong value")
			t.Fatal()
		}
	}
}
