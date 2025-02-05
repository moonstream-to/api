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

type ChainInfo struct {
	ChainID       string        `json:"chain_id"`
	CanonicalName string        `json:"canonical_name"`
	ImageURL      string        `json:"image_url"`
	Balances      ChainBalances `json:"balances"`
}

// Map of blockchain -> token balances
type BalancesResponse map[string]ChainInfo

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

	var result []interface{}
	err = session.Contract.Multicall3Caller.contract.Call(&session.CallOpts, &result, "tryBlockAndAggregate", false, calls)
	if err != nil {
		return nil, fmt.Errorf("multicall failed: %v", err)
	}

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

	// get supported blockchains which are present in contractsConfig
	supportedBlockchainsFiltered := make(map[string]bool)
	for blockchain := range contractsConfig {
		if _, ok := supportedBlockchains[blockchain]; ok {
			supportedBlockchainsFiltered[blockchain] = true
		}
	}

	// Process each blockchain in parallel
	for blockchain := range supportedBlockchainsFiltered {
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

			// Connect to client
			client, err := ethclient.Dial(node.Endpoint.String())
			if err != nil {
				resultChan <- chainResult{blockchain: blockchain, err: fmt.Errorf("failed to connect: %v", err)}
				return
			}
			defer client.Close()

			// Initialize chain balances
			chainBalances := make(ChainBalances)

			// Get native token balance first
			nativeBalance, err := client.BalanceAt(chainCtx, common.HexToAddress(checksumAddress), nil)
			if err != nil {
				log.Printf("Failed to get native balance for %s: %v", blockchain, err)
			} else {
				nativeSymbol := getNativeTokenSymbol(blockchain)
				chainBalances[nativeSymbol] = nativeBalance.String()
			}

			// Get token list for this blockchain
			tokens := getTokenList(blockchain)
			if len(tokens) > 0 {
				// Try Multicall3 first for ERC20 tokens
				tokenBalances, err := getBalancesMulticall(chainCtx, client, tokens, checksumAddress, blockchain)
				if err != nil {
					// Fallback to individual calls
					tokenBalances, err = getBalancesFallback(chainCtx, client, tokens, checksumAddress)
					if err != nil {
						resultChan <- chainResult{blockchain: blockchain, err: err}
						return
					}
				}
				// Merge token balances into chain balances
				for token, balance := range tokenBalances {
					chainBalances[token] = balance
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
			response[contractsConfig[result.blockchain].ChainID] = ChainInfo{
				ChainID:       contractsConfig[result.blockchain].ChainID,
				CanonicalName: result.blockchain,
				ImageURL:      contractsConfig[result.blockchain].ImageURL,
				Balances:      result.balances,
			}
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

func getNativeTokenSymbol(blockchain string) string {
	if chain, ok := contractsConfig[blockchain]; ok {
		return chain.NativeToken
	}
	return ""
}
