/*
Configurations for load balancer server.
*/
package configs

import (
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

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

var MOONSTREAM_NODES_SERVER_PORT = os.Getenv("MOONSTREAM_NODES_SERVER_PORT")
var MOONSTREAM_CLIENT_ID_HEADER = os.Getenv("MOONSTREAM_CLIENT_ID_HEADER")

func checkEnvVarSet() {
	if MOONSTREAM_CLIENT_ID_HEADER == "" {
		MOONSTREAM_CLIENT_ID_HEADER = "x-moonstream-client-id"
	}

	if MOONSTREAM_NODES_SERVER_PORT == "" {
		log.Fatal("Environment variable MOONSTREAM_NODES_SERVER_PORT not set")
	}
}

// Return list of NodeConfig structures
func (nc *NodeConfigList) InitNodeConfigList(configPath string) {
	checkEnvVarSet()

	rawBytes, err := ioutil.ReadFile(configPath)
	if err != nil {
		log.Fatalf("Unable to read config file, %v", err)
	}
	text := string(rawBytes)
	lines := strings.Split(text, "\n")

	// Define available blockchain nodes
	for _, line := range lines {
		fields := strings.Split(line, ",")
		if len(fields) == 3 {
			port, err := strconv.ParseInt(fields[2], 0, 16)
			if err != nil {
				log.Printf("Unable to parse port number, %v", err)
				continue
			}

			nc.Configs = append(nc.Configs, NodeConfig{
				Blockchain: fields[0],
				Addr:       fields[1],
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
