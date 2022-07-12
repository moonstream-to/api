package main

var (
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

type BlockchainConfig struct {
	Blockchain string
	IPs        []string
	Port       string
}
