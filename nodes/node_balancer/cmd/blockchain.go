package cmd

import (
	"fmt"
	"log"
	"strconv"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var (
	nodeConfigs NodeConfigs

	ALLOWED_METHODS = []string{
		"eth_blockNumber",
		"eth_call",
		"eth_chainId",
		"eth_estimateGas",
		"eth_feeHistory",
		"eth_gasPrice",
		"eth_getBalance",
		"eth_getBlockByHash",
		"eth_getBlockByNumber",
		"eth_getBlockTransactionCountByHash",
		"eth_getBlockTransactionCountByNumber",
		"eth_getCode",
		"eth_getLogs",
		"eth_getStorageAt",
		"eth_getTransactionByHash",
		"eth_getTransactionByBlockHashAndIndex",
		"eth_getTransactionByBlockNumberAndIndex",
		"eth_getTransactionCount",
		"eth_getTransactionReceipt",
		"eth_getUncleByBlockHashAndIndex",
		"eth_getUncleByBlockNumberAndIndex",
		"eth_getUncleCountByBlockHash",
		"eth_getUncleCountByBlockNumber",
		"eth_getWork",
		"eth_mining",
		// "eth_sendRawTransaction",
		"eth_protocolVersion",
		"eth_syncing",

		"net_listening",
		"net_peerCount",
		"net_version",

		"web3_clientVersion",
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

func verifyMethodWhitelisted(method string) error {
	for _, m := range ALLOWED_METHODS {
		if method == m {
			return nil
		}
	}
	return fmt.Errorf("Method not allowed")
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
