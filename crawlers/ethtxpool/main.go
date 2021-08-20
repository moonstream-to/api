package main

import (
	// "encoding/json"
	// "encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"

	// "github.com/ethereum/go-ethereum/core/types"
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

var ReportTitle string = "Ethereum: Pending transaction"

// Fetch list of transactions form Ethereum TxPool
func PollTxpoolContent(gethClient *rpc.Client, interval int) {
	currentTransactions := make(map[common.Hash]bool)

	// Structure of the map:
	// {pending | queued} -> "from" address -> nonce -> Transaction
	var result map[string]map[string]map[uint64]*Transaction

	for {
		fmt.Println("Checking pending transactions in node:")
		gethClient.Call(&result, "txpool_content")
		pendingTransactions := result["pending"]

		cacheSize := 0
		for transactionHash, _ := range currentTransactions {
			currentTransactions[transactionHash] = false
			cacheSize++
		}
		fmt.Printf("\tSize of pending transactions cache at the beginning: %d\n", cacheSize)

		addedTransactions := 0
		// Iterate over fetched result
		for fromAddress, transactionsByNonce := range pendingTransactions {
			for nonce, transaction := range transactionsByNonce {
				pendingTx := PendingTransaction{From: fromAddress, Nonce: nonce, Transaction: transaction}

				transactionHash := transaction.Hash
				_, transactionProcessed := currentTransactions[transactionHash]
				if !transactionProcessed {
					_, jsonErr := json.Marshal(pendingTx)
					if jsonErr != nil {
						fmt.Fprintf(os.Stderr, "Error marshalling pending transaction to JSON:\n%v\n", pendingTx)
						continue
					}

					// TODO(kompotkot, zomglings): Humbug API (on Spire) support bulk publication of reports. We should modify
					// Humbug go client to use the bulk publish endpoint. Currently, if we have to publish all transactions
					// pending in txpool, we *will* get rate limited. We may want to consider adding a publisher to the
					// Humbug go client that can listen on a channel and will handle rate limiting, bulk publication etc. itself
					// (without user having to worry about it).

					// report := humbug.Report{
					// 	Title:   ReportTitle,
					// 	Content: string(contents),
					// 	Tags:    []string{"lol"},
					// }
					// reporter.Publish(report)
					addedTransactions++
				}
				currentTransactions[transactionHash] = true
			}
		}
		fmt.Printf("\tAdded transactions: %d\n", addedTransactions)

		droppedTransactions := 0
		for transactionHash, justProcessed := range currentTransactions {
			if !justProcessed {
				delete(currentTransactions, transactionHash)
				droppedTransactions++
			}
		}
		fmt.Printf("\tDropped transactions: %d\n", droppedTransactions)
		fmt.Printf("Sleeping for %d seconds\n", interval)
		time.Sleep(time.Duration(interval) * time.Second)
	}
}

func main() {
	var gethConnectionString string
	var intervalSeconds int
	flag.StringVar(&gethConnectionString, "geth", "", "Geth IPC path/RPC url/Websockets URL")
	flag.IntVar(&intervalSeconds, "interval", 1, "Number of seconds to wait between RPC calls to query the transaction pool (default: 1)")
	flag.Parse()

	// Set connection with Ethereum blockchain via geth
	gethClient, err := rpc.Dial(gethConnectionString)
	if err != nil {
		panic(fmt.Sprintf("Could not connect to geth: %s", err.Error()))
	}
	defer gethClient.Close()

	// reporter, err := humbugClientFromEnv()
	// if err != nil {
	// 	panic(fmt.Sprintf("Invalid Humbug configuration: %s", err.Error()))
	// }

	PollTxpoolContent(gethClient, intervalSeconds)
}
