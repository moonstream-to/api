/*
Configurations for load balancer server.
*/
package configs

import (
	"log"
	"os"
	"strconv"
	"time"
)

// Bugout config
var BUGOUT_AUTH_URL = os.Getenv("BUGOUT_AUTH_URL")
var BUGOUT_NODE_BALANCER_APPLICATION_ID = os.Getenv("BUGOUT_NODE_BALANCER_APPLICATION_ID")
var BUGOUT_INTERNAL_CRAWLERS_USER_ID = os.Getenv("BUGOUT_INTERNAL_CRAWLERS_USER_ID")
var BUGOUT_AUTH_CALL_TIMEOUT = time.Second * 1

// Node config
type BlockchainConfig struct {
	Blockchain string
	IPs        []string
	Port       string
}

type NodeConfig struct {
	Blockchain string
	Addr       string
	Port       uint16
}

type NodeConfigList struct {
	Configs []NodeConfig
}

var ConfigList NodeConfigList

var MOONSTREAM_NODE_ETHEREUM_A_IPC_ADDR = os.Getenv("MOONSTREAM_NODE_ETHEREUM_A_IPC_ADDR")
var MOONSTREAM_NODE_ETHEREUM_B_IPC_ADDR = os.Getenv("MOONSTREAM_NODE_ETHEREUM_B_IPC_ADDR")
var MOONSTREAM_NODE_POLYGON_A_IPC_ADDR = os.Getenv("MOONSTREAM_NODE_POLYGON_A_IPC_ADDR")
var MOONSTREAM_NODE_POLYGON_B_IPC_ADDR = os.Getenv("MOONSTREAM_NODE_POLYGON_B_IPC_ADDR")
var MOONSTREAM_NODES_SERVER_PORT = os.Getenv("MOONSTREAM_NODES_SERVER_PORT")
var MOONSTREAM_CLIENT_ID_HEADER = os.Getenv("MOONSTREAM_CLIENT_ID_HEADER")

func checkEnvVarSet() {
	if MOONSTREAM_NODE_ETHEREUM_A_IPC_ADDR == "" {
		MOONSTREAM_NODE_ETHEREUM_A_IPC_ADDR = "a.ethereum.moonstream.internal"
	}
	if MOONSTREAM_NODE_ETHEREUM_B_IPC_ADDR == "" {
		MOONSTREAM_NODE_ETHEREUM_B_IPC_ADDR = "b.ethereum.moonstream.internal"
	}

	if MOONSTREAM_NODE_POLYGON_A_IPC_ADDR == "" {
		MOONSTREAM_NODE_POLYGON_A_IPC_ADDR = "a.polygon.moonstream.internal"
	}
	if MOONSTREAM_NODE_POLYGON_B_IPC_ADDR == "" {
		MOONSTREAM_NODE_POLYGON_B_IPC_ADDR = "b.polygon.moonstream.internal"
	}

	if MOONSTREAM_CLIENT_ID_HEADER == "" {
		MOONSTREAM_CLIENT_ID_HEADER = "x-moonstream-client-id"
	}

	if MOONSTREAM_NODES_SERVER_PORT == "" {
		log.Fatal("MOONSTREAM_NODES_SERVER_PORT environment variable not set")
	}
}

// Return list of NodeConfig structures
func (nc *NodeConfigList) InitNodeConfigList() {
	checkEnvVarSet()

	// Define available blockchain nodes
	blockchainConfigList := make([]BlockchainConfig, 0, 2)
	blockchainConfigList = append(blockchainConfigList, BlockchainConfig{
		Blockchain: "ethereum",
		IPs:        []string{MOONSTREAM_NODE_ETHEREUM_A_IPC_ADDR, MOONSTREAM_NODE_ETHEREUM_B_IPC_ADDR},
		Port:       "8545",
	})
	blockchainConfigList = append(blockchainConfigList, BlockchainConfig{
		Blockchain: "polygon",
		IPs:        []string{MOONSTREAM_NODE_POLYGON_A_IPC_ADDR, MOONSTREAM_NODE_POLYGON_B_IPC_ADDR},
		Port:       "8545",
	})

	// Parse node addr, ip and blockchain
	for _, b := range blockchainConfigList {
		for _, nodeIP := range b.IPs {
			port, err := strconv.ParseInt(b.Port, 0, 16)
			if err != nil {
				log.Printf("Unable to parse port number: %s", b.Port)
				continue
			}
			nc.Configs = append(nc.Configs, NodeConfig{
				Blockchain: b.Blockchain,
				Addr:       nodeIP,
				Port:       uint16(port),
			})
		}
	}
}

var NB_CONNECTION_RETRIES = 2
var NB_CONNECTION_RETRIES_INTERVAL = time.Millisecond * 10
var NB_HEALTH_CHECK_INTERVAL = time.Second * 5
var NB_HEALTH_CHECK_CALL_TIMEOUT = time.Second * 2

// Client config
var NB_CLIENT_NODE_KEEP_ALIVE = int64(5) // How long to store node in hot list for client in seconds

// Humbug config
var HUMBUG_REPORTER_NODE_BALANCER_TOKEN = os.Getenv("HUMBUG_REPORTER_NODE_BALANCER_TOKEN")

// Database config
var MOONSTREAM_DB_URI = os.Getenv("MOONSTREAM_DB_URI")
