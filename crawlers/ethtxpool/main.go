package main

import (
	// "encoding/json"
	// "encoding/hex"
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

type txJSON struct {
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
	From        string  `json:"from"`
	Nonce       uint64  `json:"nonce"`
	Transaction *txJSON `json:"transaction"`
}

type PendingTransactions struct {
	Transactions PendingTransaction `json:"transactions"`
}

var ReportTitle string = "Ethereum: Pending transaction"

// Fetch list of transactions form Ethereum TxPool
// func TxPoolCall(gethClient *rpc.Client) (pendingTxsNew []PendingTransaction) {
func TxPoolCall(gethClient *rpc.Client) {
	pendingTxsOld := make([]PendingTransaction, 0, 6000) 	// List of transactions from previous iteration
	pendingTxsNew := make([]PendingTransaction, 0, 6000) 	// Empty list for new incoming transactions

	var result map[string]map[string]map[uint64]*txJSON

	for {
		gethClient.Call(&result, "txpool_content")
		pendingTransactions := result["pending"]

		// Iterate over fetched result
		for fromAddress, transactionsByNonce := range pendingTransactions {
			for nonce, transaction := range transactionsByNonce {
				pendingTx := PendingTransaction{From: fromAddress, Nonce: nonce, Transaction: transaction}

				pendingTxsNew = append(pendingTxsNew, pendingTx) // Add to list of new incoming transactions

				// Check if transaction in old list of transactions,
				// then remove from it
				for oldTxInd, oldTx := range pendingTxsOld {
					if pendingTx.Transaction.Hash == oldTx.Transaction.Hash {
						pendingTxsOld[oldTxInd] = pendingTxsOld[len(pendingTxsOld)-1]
						// pendingTxsOld[len(pendingTxsOld)-1] = ""   // Erase last element (write zero value) TODO: not sure I should do it
						pendingTxsOld = pendingTxsOld[:len(pendingTxsOld)-1]
					} else {
						// send to humbug
					}
				}

				// _, jsonErr := json.Marshal(pendingTx)
				// if jsonErr != nil {
				// 	fmt.Fprintf(os.Stderr, "Error marshalling pending transaction to JSON:\n%v\n", pendingTx)
				// 	continue
				// }
				// fmt.Println(transactionHash)
				// // report := humbug.Report{
				// // 	Title:   ReportTitle,
				// // 	Content: string(contents),
				// // 	Tags:    []string{"lol"},
				// // }
				// // reporter.Publish(report)
			}
		}
		// - For loop through pendingTxsOld to mark in humbug as old

		// - Clean old slice
		pendingTxsOld = pendingTxsOld[:0]

		fmt.Println("New:", len(pendingTxsNew))
		// - Copy new slice to old
		copy(pendingTxsOld, pendingTxsNew)

		fmt.Println("New:", len(pendingTxsNew))
		// - Clean new slice
		pendingTxsNew = pendingTxsNew[:0]

		fmt.Println("New:", len(pendingTxsNew))
		fmt.Println("Old:", len(pendingTxsOld))
		time.Sleep(3 * time.Second)
	}

	// return
}

func main() {
	var gethConnectionString string
	flag.StringVar(&gethConnectionString, "geth", "", "Geth IPC path/RPC url/Websockets URL")
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

	// TODO(kompotkot, zomglings): We should cache pending transactions in memory and only publish reports
	// for new transactions. When this process starts up, it should pull the most recent (within last 5 minutes -- tunable)
	// reported pending transactions from the Humbug journal (will require a read token) and load them
	// into the cache.

	// TODO(kompotkot, zomglings): Humbug API (on Spire) support bulk publication of reports. We should modify
	// Humbug go client to use the bulk publish endpoint. Currently, if we have to publish all transactions
	// pending in txpool, we *will* get rate limited. We may want to consider adding a publisher to the
	// Humbug go client that can listen on a channel and will handle rate limiting, bulk publication etc. itself
	// (without user having to worry about it).

	// TODO(kompotkot, zomglings): Right now, we are only working with "pending" transactions. Ethereum
	// TXPool data structure also has "queued" transactions. What is the difference between "pending" and
	// "queued" and should we be reporting "queued" transaction as well?

	// pendingHashList := []common.Hash
	// updatedPendingHashList := []common.Hash

	// var result map[string]map[string]map[uint64]*txJSON

	// gethClient.Call(&result, "txpool_content")
	// pendingTransactions := result["pending"]

	// for fromAddress, transactionsByNonce := range pendingTransactions {
	// 	for nonce, transaction := range transactionsByNonce {
	// 		pendingTx := PendingTransaction{From: fromAddress, Nonce: nonce, Transaction: transaction}
	// 		// pendingTransactionsRes := append(pendingTransactionsRes, pendingTx)
	// 		fmt.Println(pendingTx.Transaction.GasPrice)

	// 		contents, jsonErr := json.Marshal(pendingTx)
	// 		if jsonErr != nil {
	// 			fmt.Fprintf(os.Stderr, "Error marshalling pending transaction to JSON:\n%v\n", pendingTx)
	// 			continue
	// 		}
	// 		fmt.Println(string(contents))
	// 		// // report := humbug.Report{
	// 		// // 	Title:   ReportTitle,
	// 		// // 	Content: string(contents),
	// 		// // 	Tags:    []string{"lol"},
	// 		// // }
	// 		// // reporter.Publish(report)
	// 	}
	// 	break
	// }

	TxPoolCall(gethClient)
	// pendingTransactions := TxPoolCall(gethClient)
	// fmt.Println(len(pendingTransactions))

	// transactionHash := transaction.Hash
	// for h := range pendingHashList{
	// 	if h == transactionHash {
	// 		updatedPendingHashList
	// 	}
	// }

}
