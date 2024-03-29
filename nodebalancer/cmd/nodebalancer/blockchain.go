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
		"eth_sendRawTransaction":                  true,
		"eth_protocolVersion":                     true,
		"eth_syncing":                             true,

		"net_listening": true,
		"net_peerCount": true,
		"net_version":   true,

		"web3_clientVersion": true,

		// zksync methods
		"zks_estimateFee":             true,
		"zks_estimateGasL1ToL2":       true,
		"zks_getAllAccountBalances":   true,
		"zks_getBlockDetails":         true,
		"zks_getBridgeContracts":      true,
		"zks_getBytecodeByHash":       true,
		"zks_getConfirmedTokens":      true,
		"zks_getL1BatchBlockRange":    true,
		"zks_getL1BatchDetails":       true,
		"zks_getL2ToL1LogProof":       true,
		"zks_getL2ToL1MsgProof":       true,
		"zks_getMainContract":         true,
		"zks_getRawBlockTransactions": true,
		"zks_getTestnetPaymaster":     true,
		"zks_getTokenPrice":           true,
		"zks_getTransactionDetails":   true,
		"zks_L1BatchNumber":           true,
		"zks_L1ChainId":               true,

		// starknet methods
		"starknet_specVersion":                     true,
		"starknet_getBlockWithTxHashes":            true,
		"starknet_getBlockWithTxs":                 true,
		"starknet_getStateUpdate":                  true,
		"starknet_getStorageAt":                    true,
		"starknet_getTransactionStatus":            true,
		"starknet_getTransactionByHash":            true,
		"starknet_getTransactionByBlockIdAndIndex": true,
		"starknet_getTransactionReceipt":           true,
		"starknet_getClass":                        true,
		"starknet_getClassHashAt":                  true,
		"starknet_getClassAt":                      true,
		"starknet_getBlockTransactionCount":        true,
		"starknet_call":                            true,
		"starknet_estimateFee":                     true,
		"starknet_estimateMessageFee":              true,
		"starknet_blockNumber":                     true,
		"starknet_blockHashAndNumber":              true,
		"starknet_chainId":                         true,
		"starknet_syncing":                         true,
		"starknet_getEvents":                       true,
		"starknet_getNonce":                        true,

		"starknet_traceTransaction":       true,
		"starknet_simulateTransactions":   true,
		"starknet_traceBlockTransactions": true,

		"starknet_addInvokeTransaction":        true,
		"starknet_addDeclareTransaction":       true,
		"starknet_addDeployAccountTransaction": true,
	}
)

type JSONRPCRequest struct {
	Jsonrpc string      `json:"jsonrpc"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params"`
	ID      interface{} `json:"id"` // According to the JSON-RPC specification, the id can be a string, number, or null
}

type BlockchainConfig struct {
	Blockchain string
	IPs        []string
	Port       string
}
