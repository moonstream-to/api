package cmd

import (
	"log"
	"strconv"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var (
	nodeConfigs NodeConfigs

	ALLOWED_METHODS = map[string]bool{
		"eth_blockNumber":                         true,
		"eth_call":                                true,
		"eth_chainId":                             true,
		"eth_estimateGas":                         true,
		"eth_feeHistory":                          true,
		"eth_gasPrice":                            true,
		"eth_getBalance":                          true,
		"eth_getBlockByHash":                      true,
		"eth_getBlockByNumber":                    true,
		"eth_getBlockTransactionCountByHash":      true,
		"eth_getBlockTransactionCountByNumber":    true,
		"eth_getCode":                             true,
		"eth_getLogs":                             true,
		"eth_getStorageAt":                        true,
		"eth_getTransactionByHash":                true,
		"eth_getTransactionByBlockHashAndIndex":   true,
		"eth_getTransactionByBlockNumberAndIndex": true,
		"eth_getTransactionCount":                 true,
		"eth_getTransactionReceipt":               true,
		"eth_getUncleByBlockHashAndIndex":         true,
		"eth_getUncleByBlockNumberAndIndex":       true,
		"eth_getUncleCountByBlockHash":            true,
		"eth_getUncleCountByBlockNumber":          true,
		"eth_getWork":                             true,
		"eth_mining":                              true,
		// "eth_sendRawTransaction": true,
		"eth_protocolVersion": true,
		"eth_syncing":         true,

		"net_listening": true,
		"net_peerCount": true,
		"net_version":   true,

		"web3_clientVersion": true,
	}
)

type JSONRPCRequest struct {
	Jsonrpc string        `json:"jsonrpc"`
	Method  string        `json:"method"`
	Params  []interface{} `json:"params"`
	ID      uint64        `json:"id"`
}

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
