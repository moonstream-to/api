/*
Ethereum blockchain transaction pool crawler.

Execute:
go run main.go -geth http://127.0.0.1:8545
*/
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"

	humbug "ethtxpool/humbug"
	// humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"

	"github.com/ethereum/go-ethereum/rpc"
	"github.com/google/uuid"
)

// Generate humbug client to be able write data in Bugout journal.
func humbugClientFromEnv() (*humbug.HumbugReporter, error) {
	clientID := os.Getenv("ETHTXPOOL_HUMBUG_CLIENT_ID")
	humbugToken := os.Getenv("ETHTXPOOL_HUMBUG_TOKEN")
	sessionID := uuid.New().String()

	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err := humbug.CreateHumbugReporter(consent, clientID, sessionID, humbugToken)
	return reporter, err
}

type Transaction struct {
	Type hexutil.Uint64 `json:"type"`

	// Common transaction fields:
	Nonce                *hexutil.Uint64 `json:"nonce"`
	GasPrice             *hexutil.Big    `json:"gasPrice"`
	MaxPriorityFeePerGas *hexutil.Big    `json:"maxPriorityFeePerGas"`
	MaxFeePerGas         *hexutil.Big    `json:"maxFeePerGas"`
	Gas                  *hexutil.Uint64 `json:"gas"`
	Value                *hexutil.Big    `json:"value"`
	Data                 *hexutil.Bytes  `json:"input"`
	V                    *hexutil.Big    `json:"v"`
	R                    *hexutil.Big    `json:"r"`
	S                    *hexutil.Big    `json:"s"`
	To                   *common.Address `json:"to"`

	// Access list transaction fields:
	ChainID *hexutil.Big `json:"chainId,omitempty"`
	// AccessList *AccessList  `json:"accessList,omitempty"`

	// Only used for encoding:
	Hash common.Hash `json:"hash"`
}

type PendingTransaction struct {
	From        string       `json:"from"`
	Nonce       uint64       `json:"nonce"`
	Transaction *Transaction `json:"transaction"`
}

type PendingTransactions struct {
	Transactions PendingTransaction `json:"transactions"`
}

// Fetch list of transactions form Ethereum TxPool
func PollTxpoolContent(gethClient *rpc.Client, interval int, longIntervalSeconds int, reporter *humbug.HumbugReporter) {
	currentTransactions := make(map[common.Hash]bool)

	// Structure of the map:
	// {pending | queued} -> "from" address -> nonce -> Transaction
	var result map[string]map[string]map[uint64]*Transaction

	for {
		fmt.Println("Checking pending transactions in node:")
		gethClient.Call(&result, "txpool_content")
		pendingTransactions := result["pending"]

		// Mark all transactions from previous iteration as false
		cacheSize := 0
		for transactionHash, _ := range currentTransactions {
			currentTransactions[transactionHash] = false
			cacheSize++
		}
		fmt.Printf("\tSize of pending transactions cache at the beginning: %d\n", cacheSize)

		reports := []humbug.Report{}

		// Iterate over fetched result
		addedTransactionsCounter := 0
		for fromAddress, transactionsByNonce := range pendingTransactions {
			for nonce, transaction := range transactionsByNonce {
				pendingTx := PendingTransaction{From: fromAddress, Nonce: nonce, Transaction: transaction}

				transactionHash := transaction.Hash
				_, transactionProcessed := currentTransactions[transactionHash]
				if !transactionProcessed {
					contents, jsonErr := json.Marshal(pendingTx)
					if jsonErr != nil {
						fmt.Fprintf(os.Stderr, "Error marshalling pending transaction to JSON:\n%v\n", pendingTx)
						continue
					}

					// TODO(kompotkot, zomglings): Humbug API (on Spire) support bulk publication of reports. We should modify
					// Humbug go client to use the bulk publish endpoint. Currently, if we have to publish all transactions
					// pending in txpool, we *will* get rate limited. We may want to consider adding a publisher to the
					// Humbug go client that can listen on a channel and will handle rate limiting, bulk publication etc. itself
					// (without user having to worry about it).
					ReportTitle := "Ethereum: Pending transaction: " + transactionHash.String()
					ReportTags := []string{
						"hash:" + transactionHash.String(),
						"from_address:" + fromAddress,
						fmt.Sprintf("to_address:%s", pendingTx.Transaction.To),
						fmt.Sprintf("gas_price:%d", pendingTx.Transaction.GasPrice.ToInt()),
						fmt.Sprintf("max_priority_fee_per_gas:%d", pendingTx.Transaction.MaxPriorityFeePerGas.ToInt()),
						fmt.Sprintf("max_fee_per_gas:%d", pendingTx.Transaction.MaxFeePerGas.ToInt()),
						fmt.Sprintf("gas:%d", pendingTx.Transaction.Gas),
					}
					report := humbug.Report{
						Title:   ReportTitle,
						Content: string(contents),
						Tags:    ReportTags,
					}
					reports = append(reports, report)
					addedTransactionsCounter++
				}
				currentTransactions[transactionHash] = true
			}
		}
		reporter.PublishBulk(reports)
		fmt.Printf("\tPublished transactions: %d\n", addedTransactionsCounter)

		// Clean the slice out of disappeared transactions
		droppedTransactionsCounter := 0
		for transactionHash, justProcessed := range currentTransactions {
			if !justProcessed {
				delete(currentTransactions, transactionHash)
				// TODO(kompotkot): Add humbug andpoint to modify entry tags as
				// "processed" transaction
				droppedTransactionsCounter++
			}
		}
		fmt.Printf("\tDropped transactions: %d\n", droppedTransactionsCounter)

		if addedTransactionsCounter >= 2500 {
			fmt.Printf("Sleeping for %d seconds\n", longIntervalSeconds)
			time.Sleep(time.Duration(longIntervalSeconds) * time.Second)
		} else {
			fmt.Printf("Sleeping for %d seconds\n", interval)
			time.Sleep(time.Duration(interval) * time.Second)
		}
	}
}

func main() {
	var gethConnectionString string
	var intervalSeconds int
	var longIntervalSeconds int
	flag.StringVar(&gethConnectionString, "geth", "", "Geth IPC path/RPC url/Websockets URL")
	flag.IntVar(&longIntervalSeconds, "long_interval", 10, "Number of seconds to wait between RPC calls if number of processed transactions greater then 2500 (default: 10)")
	flag.IntVar(&intervalSeconds, "interval", 1, "Number of seconds to wait between RPC calls to query the transaction pool (default: 1)")
	flag.Parse()

	// Set connection with Ethereum blockchain via geth
	gethClient, err := rpc.Dial(gethConnectionString)
	if err != nil {
		panic(fmt.Sprintf("Could not connect to geth: %s", err.Error()))
	}
	defer gethClient.Close()

	reporter, err := humbugClientFromEnv()
	if err != nil {
		panic(fmt.Sprintf("Invalid Humbug configuration: %s", err.Error()))
	}

	PollTxpoolContent(gethClient, intervalSeconds, longIntervalSeconds, reporter)
}
