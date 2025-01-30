package main

import (
	"context"
	"fmt"
	"log"
	"math/big"
	"sync"
	"time"

	ethereum "github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

type TokenBalance struct {
	Address string `json:"address"`
	Balance string `json:"balance"`
}

type ChainBalances map[string]string

// Map of blockchain -> token balances
type BalancesResponse map[string]ChainBalances

type chainResult struct {
	blockchain string
	balances   ChainBalances
	err        error
}

// getBalancesMulticall queries token balances using Multicall3
func getBalancesMulticall(ctx context.Context, client *ethclient.Client, tokens []string, checksumAddress string, blockchain string) (ChainBalances, error) {
	chainBalances := make(ChainBalances)

	// Get Multicall3 contract address
	multicallAddr := getMulticall3Address(blockchain)
	if multicallAddr == "" {
		return nil, fmt.Errorf("multicall3 not supported for blockchain %s", blockchain)
	}

	// Create Multicall3 contract instance
	multicallAddress := common.HexToAddress(multicallAddr)
	mc3, err := NewMulticall3(multicallAddress, client)
	if err != nil {
		return nil, fmt.Errorf("failed to create multicall3 contract: %v", err)
	}

	// Prepare calls for each token
	calls := make([]Multicall3Call, len(tokens))
	for i, token := range tokens {
		callData := createBalanceOfCallData(checksumAddress)
		calls[i] = Multicall3Call{
			Target:   common.HexToAddress(token),
			CallData: callData,
		}
	}

	session := Multicall3Session{
		Contract: mc3,
		CallOpts: bind.CallOpts{Context: ctx},
	}

	// Solidity: function tryBlockAndAggregate(bool requireSuccess, (address,bytes)[] calls) payable returns(uint256 blockNumber, bytes32 blockHash, (bool,bytes)[] returnData)
	var result []interface{}
	err = session.Contract.Multicall3Caller.contract.Call(&session.CallOpts, &result, "tryBlockAndAggregate", false, calls)
	if err != nil {
		return nil, fmt.Errorf("multicall failed: %v", err)
	}

	// tryBlockAndAggregate returns (uint256 blockNumber, bytes32 blockHash, (bool,bytes)[] returnData)
	if len(result) != 3 {
		return nil, fmt.Errorf("unexpected result length: got %d, want 3", len(result))
	}

	returnData := result[2].([]struct {
		Success    bool   `json:"success"`
		ReturnData []byte `json:"returnData"`
	})

	for i, data := range returnData {
		if data.Success && len(data.ReturnData) > 0 {
			balance := new(big.Int)
			balance.SetBytes(data.ReturnData)
			chainBalances[tokens[i]] = balance.String()
		}
	}

	return chainBalances, nil
}

// getBalances fetches token balances across all supported blockchains
func getBalances(ctx context.Context, address string) (BalancesResponse, error) {
	if !common.IsHexAddress(address) {
		return nil, fmt.Errorf("invalid ethereum address")
	}

	// Convert to checksum address
	checksumAddress := common.HexToAddress(address).Hex()

	// Initialize response
	response := make(BalancesResponse)

	// Create channel for collecting results
	resultChan := make(chan chainResult)

	// Count active goroutines
	var wg sync.WaitGroup

	// Process each blockchain in parallel
	for blockchain := range supportedBlockchains {
		wg.Add(1)
		go func(blockchain string) {
			defer wg.Done()

			// Create timeout context
			chainCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
			defer cancel()

			// Get the node for this blockchain
			node := blockchainPool.GetNextNode(blockchain)
			if node == nil {
				resultChan <- chainResult{blockchain: blockchain, err: fmt.Errorf("no available node")}
				return
			}

			// Get token list for this blockchain
			tokens := getTokenList(blockchain)
			if len(tokens) == 0 {
				resultChan <- chainResult{blockchain: blockchain, balances: make(ChainBalances)}
				return
			}

			// Connect to client
			client, err := ethclient.Dial(node.Endpoint.String())
			if err != nil {
				resultChan <- chainResult{blockchain: blockchain, err: fmt.Errorf("failed to connect: %v", err)}
				return
			}
			defer client.Close()

			// Try Multicall3 first
			chainBalances, err := getBalancesMulticall(chainCtx, client, tokens, checksumAddress, blockchain)
			if err != nil {
				// Fallback to individual calls
				chainBalances, err = getBalancesFallback(chainCtx, client, tokens, checksumAddress)
				if err != nil {
					resultChan <- chainResult{blockchain: blockchain, err: err}
					return
				}
			}

			select {
			case <-chainCtx.Done():
				resultChan <- chainResult{blockchain: blockchain, err: fmt.Errorf("timeout exceeded")}
			case resultChan <- chainResult{blockchain: blockchain, balances: chainBalances}:
			}
		}(blockchain)
	}

	// Close results channel when all goroutines are done
	go func() {
		wg.Wait()
		close(resultChan)
	}()

	// Collect results
	for result := range resultChan {
		if result.err != nil {
			log.Printf("Error fetching balances for %s: %v", result.blockchain, result.err)
			continue
		}
		if len(result.balances) > 0 {
			response[result.blockchain] = result.balances
		}
	}

	return response, nil
}

// getBalancesFallback queries token balances one by one
func getBalancesFallback(ctx context.Context, client *ethclient.Client, tokens []string, checksumAddress string) (ChainBalances, error) {
	chainBalances := make(ChainBalances)
	for _, token := range tokens {
		select {
		case <-ctx.Done():
			return chainBalances, fmt.Errorf("timeout exceeded")
		default:
			callData := createBalanceOfCallData(checksumAddress)
			tokenAddr := common.HexToAddress(token)
			result, err := client.CallContract(ctx, ethereum.CallMsg{
				To:   &tokenAddr,
				Data: callData,
			}, nil)
			if err != nil {
				log.Printf("Failed to get balance for token %s: %v", token, err)
				continue
			}
			if len(result) > 0 {
				balance := new(big.Int)
				balance.SetBytes(result)
				chainBalances[token] = balance.String()
			}
		}
	}
	return chainBalances, nil
}

// Helper functions

func createBalanceOfCallData(address string) []byte {
	// ERC20 balanceOf function signature: balanceOf(address)
	methodID := crypto.Keccak256([]byte("balanceOf(address)"))[0:4]

	// Pack address parameter
	paddedAddress := common.LeftPadBytes(common.HexToAddress(address).Bytes(), 32)

	// Combine method ID and parameters
	return append(methodID, paddedAddress...)
}

// func getTokenList(blockchain string) []string {
// 	// TODO: This should be moved to a configuration file
// 	switch blockchain {
// 	case "ethereum":
// 		return []string{
// 			"0x0000000000000000000000000000000000000000", // WETH
// 			"0x6B175474E89094C44Da98b954EedeAC495271d0F", // DAI
// 			"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
// 			"0xdAC17F958D2ee523a2206206994597C13D831ec7", // USDT
// 		}
// 	case "polygon":
// 		return []string{
// 			"0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270", // WMATIC
// 			"0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", // USDC
// 			"0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063", // DAI
// 			"0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619", // WETH
// 			"0xc2132D05D31c914a87C6611C10748AEb04B58e8F", // USDT
// 		}
// 	default:
// 		return nil
// 	}
// }

// func getMulticall3Address(blockchain string) string {
// 	// TODO: Move to config
// 	switch blockchain {
// 	case "ethereum":
// 		return "0xcA11bde05977b3631167028862bE2a173976CA11"
// 	case "polygon":
// 		return "0xcA11bde05977b3631167028862bE2a173976CA11"
// 	default:
// 		return ""
// 	}
// }

func getMulticall3Address(blockchain string) string {
	if chain, ok := contractsConfig[blockchain]; ok {
		return chain.Multicall3
	}
	return ""
}

func getTokenList(blockchain string) []string {
	if chain, ok := contractsConfig[blockchain]; ok {
		tokens := make([]string, 0, len(chain.Tokens))
		for _, addr := range chain.Tokens {
			tokens = append(tokens, addr)
		}
		return tokens
	}
	return nil
}
