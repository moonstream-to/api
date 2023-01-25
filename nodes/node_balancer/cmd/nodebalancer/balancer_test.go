package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"testing"
	"time"
)

var testApiUrl = os.Getenv("TEST_API_URL")

func setupBalancerSuit(t *testing.T) func(t *testing.T) {
	t.Log("Setup Balancer suit")

	testEndpoint1, err := url.Parse(fmt.Sprintf("%s/test1/jsonrpc", testApiUrl))
	if err != nil {
		t.Error(err)
	}
	testEndpoint2, err := url.Parse(fmt.Sprintf("%s/test2/jsonrpc", testApiUrl))
	if err != nil {
		t.Error(err)
	}

	testNode1 := &Node{
		Endpoint: testEndpoint1,
	}
	testNode2 := &Node{
		Endpoint: testEndpoint2,
	}

	testBlockchainPools := make(map[string]*NodePool)
	testBlockchainPools["test"] = &NodePool{
		NodesMap: make(map[string][]*Node),
	}
	testBlockchainPools["test"].NodesMap["tag_1"] = append(
		testBlockchainPools["test"].NodesMap["tag_1"], testNode1,
	)
	testBlockchainPools["test"].NodesMap["tag_2"] = append(
		testBlockchainPools["test"].NodesMap["tag_2"], testNode2,
	)
	testBlockchainPools["test"].NodesSet = append(
		testBlockchainPools["test"].NodesSet, testNode1, testNode2,
	)

	blockchainPools = make(map[string]*NodePool)
	blockchainPools = testBlockchainPools

	clientPool = make(map[string]ClientPool)

	return func(t *testing.T) {
		t.Log("Teardown suit")
	}
}

func TestHealthCheck(t *testing.T) {
	teardownSuit := setupBalancerSuit(t)
	defer teardownSuit(t)

	makeRequestToNode := func(node *Node) {
		alive := false
		httpClient := http.Client{Timeout: NB_HEALTH_CHECK_CALL_TIMEOUT}
		resp, err := httpClient.Post(
			node.Endpoint.String(),
			"application/json",
			bytes.NewBuffer([]byte(`{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}`)),
		)
		if err != nil {
			node.UpdateNodeState(0, alive)
			t.Logf("Unable to reach node: %s", node.Endpoint.Host)
		}
		defer resp.Body.Close()
	}

	NB_HEALTH_CHECK_INTERVAL = time.Millisecond * 1

	c := 0
	HealthCheck()

	go initHealthCheck()

	for c <= 1200300 {
		node := GetNextNode(
			blockchainPools["test"].NodesSet,
			blockchainPools["test"].TopNode,
		)
		makeRequestToNode(node)
		c++
	}
}
