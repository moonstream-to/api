package cmd

import (
	"log"
	"strconv"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var (
	nodeConfigs NodeConfigs
)

// Node conf
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

type NodeConfigs struct {
	NodeConfigs []NodeConfig
}

// Return list of NodeConfig structures
func (nc *NodeConfigs) InitNodeConfiguration() {
	// Define available blockchain nodes
	blockchainConfigList := make([]BlockchainConfig, 0, 2)
	blockchainConfigList = append(blockchainConfigList, BlockchainConfig{
		Blockchain: "ethereum",
		IPs:        []string{configs.MOONSTREAM_NODE_ETHEREUM_A_IPC_ADDR, configs.MOONSTREAM_NODE_ETHEREUM_B_IPC_ADDR},
		Port:       "8545",
	})
	blockchainConfigList = append(blockchainConfigList, BlockchainConfig{
		Blockchain: "polygon",
		IPs:        []string{configs.MOONSTREAM_NODE_POLYGON_A_IPC_ADDR, configs.MOONSTREAM_NODE_POLYGON_B_IPC_ADDR},
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
			nc.NodeConfigs = append(nc.NodeConfigs, NodeConfig{
				Blockchain: b.Blockchain,
				Addr:       nodeIP,
				Port:       uint16(port),
			})
		}
	}
}
