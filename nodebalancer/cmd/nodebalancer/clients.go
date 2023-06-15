package main

import (
	"log"
	"reflect"
	"sync"
	"time"
)

var (
	clientPool map[string]ClientPool
)

// Structure to define user access according with Brood resources
type ClientAccess struct {
	ResourceID string

	authorizationToken string

	ClientResourceData ClientResourceData

	LastAccessTs            int64
	LastSessionAccessTs     int64 // When last session with nodebalancer where started
	LastSessionCallsCounter int64

	requestedDataSource string
}

type ClientResourceData struct {
	UserID           string `json:"user_id"`
	AccessID         string `json:"access_id"`
	Name             string `json:"name"`
	Description      string `json:"description"`
	BlockchainAccess bool   `json:"blockchain_access"`
	ExtendedMethods  bool   `json:"extended_methods"`

	PeriodDuration    int64 `json:"period_duration"`
	PeriodStartTs     int64 `json:"period_start_ts"`
	MaxCallsPerPeriod int64 `json:"max_calls_per_period"`
	CallsPerPeriod    int64 `json:"calls_per_period"`

	Type string `json:"type"`
}

// CheckClientCallPeriodLimits returns true if limit of call requests per period is exceeded
// If client passed this check, we will add this client to cache and let him operates until cache will be
// cleaned with go-routine and resource will be updated
func (ca *ClientAccess) CheckClientCallPeriodLimits(tsNow int64) bool {
	isClientAllowedToGetAccess := false
	if tsNow-ca.ClientResourceData.PeriodStartTs < ca.ClientResourceData.PeriodDuration {
		// Client operates in period
		if ca.ClientResourceData.CallsPerPeriod+ca.LastSessionCallsCounter < ca.ClientResourceData.MaxCallsPerPeriod {
			// Client's limit of calls not reached
			isClientAllowedToGetAccess = true
		}
	} else {
		// Client period should be refreshed
		if stateCLI.enableDebugFlag {
			log.Printf("Refresh client's period_start_ts with time.now() and reset calls_per_period")
		}
		ca.ClientResourceData.CallsPerPeriod = 0
		ca.ClientResourceData.PeriodStartTs = tsNow
		isClientAllowedToGetAccess = true
	}
	return isClientAllowedToGetAccess
}

// UpdateClientResourceCallCounter updates Brood resource where increase calls counter to node
// with current number of calls during last session.
func (ca *ClientAccess) UpdateClientResourceCallCounter(tsNow int64) error {
	update := make(map[string]interface{})
	update["period_start_ts"] = ca.ClientResourceData.PeriodStartTs
	update["calls_per_period"] = ca.ClientResourceData.CallsPerPeriod + ca.LastSessionCallsCounter

	updatedResource, err := bugoutClient.Brood.UpdateResource(
		NB_CONTROLLER_TOKEN,
		ca.ResourceID,
		update,
		[]string{},
	)
	if err != nil {
		return err
	}
	log.Printf("Resource %s updated\n", updatedResource.Id)

	return nil
}

// Node - which one node client worked with
// LastCallTs - timestamp from last call
type Client struct {
	Node       *Node
	LastCallTs int64

	mux sync.RWMutex
}

// Where id is a key and equal to ClientResourceData -> AccessID
type ClientPool struct {
	Client map[string]*Client
}

// Generate pools for clients for different blockchains
func CreateClientPools() {
	clientPool = make(map[string]ClientPool)

	for b := range supportedBlockchains {
		clientPool[b] = ClientPool{}
		if cp, ok := clientPool[b]; ok {
			cp.Client = make(map[string]*Client)
			clientPool[b] = cp
		}
	}
}

// Return client pool corresponding to provided blockchain
func GetClientPool(blockchain string) *ClientPool {
	var cpool *ClientPool
	for b := range supportedBlockchains {
		if b == blockchain {
			c := clientPool[blockchain]
			cpool = &c
		}
	}
	return cpool
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
		if lastCallTs < NB_CLIENT_NODE_KEEP_ALIVE {
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
		if lastCallTs >= NB_CLIENT_NODE_KEEP_ALIVE {
			delete(cpool.Client, id)
		} else {
			cnt += 1
		}
	}

	return cnt
}
