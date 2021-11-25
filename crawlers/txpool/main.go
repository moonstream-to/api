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
	"math/big"
	"os"
	"strings"
	"time"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/params"
	"github.com/ethereum/go-ethereum/rpc"
	"github.com/google/uuid"
)

// Generate humbug client
func humbugClient(sessionID string, clientID string, humbugToken string) (*humbug.HumbugReporter, error) {
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

// Split list of reports on nested lists
func generateChunks(xs []humbug.Report, chunkSize int) [][]humbug.Report {
	if len(xs) == 0 {
		return nil
	}
	divided := make([][]humbug.Report, (len(xs)+chunkSize-1)/chunkSize)
	prev := 0
	i := 0
	till := len(xs) - chunkSize
	for prev < till {
		next := prev + chunkSize
		divided[i] = xs[prev:next]
		prev = next
		i++
	}
	divided[i] = xs[prev:]
	return divided
}

// Fetch list of transactions form Ethereum TxPool
func PollTxpoolContent(gethClient *rpc.Client, interval int, reporter *humbug.HumbugReporter, blockchain string) {
	initPoll := true
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
		for transactionHash := range currentTransactions {
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

					ReportTitle := fmt.Sprintf("%s: Pending transaction: ", strings.Title(blockchain)) + transactionHash.String()
					ReportTags := []string{
						"hash:" + transactionHash.String(),
						"from_address:" + fromAddress,
						fmt.Sprintf("to_address:%s", pendingTx.Transaction.To),
						fmt.Sprintf("gas_price:%d", pendingTx.Transaction.GasPrice.ToInt()),
						fmt.Sprintf("max_priority_fee_per_gas:%d", pendingTx.Transaction.MaxPriorityFeePerGas.ToInt()),
						fmt.Sprintf("max_fee_per_gas:%d", pendingTx.Transaction.MaxFeePerGas.ToInt()),
						fmt.Sprintf("gas:%d", pendingTx.Transaction.Gas),
						fmt.Sprintf("value:%d", new(big.Float).Quo(new(big.Float).SetInt(transaction.Value.ToInt()), big.NewFloat(params.Ether))),
						fmt.Sprintf("crawl_type:%s_txpool", blockchain),
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

		if !initPoll {
			reportChunks := generateChunks(reports, 500)
			for _, chunk := range reportChunks {
				fmt.Printf("\tPublishing chunk with: %d/%d reports\n", len(chunk), addedTransactionsCounter)
				reporter.PublishBulk(chunk)
				time.Sleep(time.Duration(interval) * time.Second)
			}

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

			fmt.Printf("Sleeping for %d seconds\n", interval)
			time.Sleep(time.Duration(interval) * time.Second)
		} else {
			fmt.Printf("Initial start of crawler, too many transactions: %d, passing them...\n", addedTransactionsCounter)
			initPoll = false
		}
	}
}

func main() {
	var blockchain string
	var intervalSeconds int
	flag.StringVar(&blockchain, "blockchain", "ethereum", "Blockchain to crawl")
	flag.IntVar(&intervalSeconds, "interval", 1, "Number of seconds to wait between RPC calls to query the transaction pool (default: 1)")
	flag.Parse()

	var MOONSTREAM_NODE_IPC_ADDR = os.Getenv(fmt.Sprintf("MOONSTREAM_NODE_%s_IPC_ADDR", strings.ToUpper(blockchain)))
	var MOONSTREAM_NODE_IPC_PORT = os.Getenv(fmt.Sprintf("MOONSTREAM_NODE_%s_IPC_PORT", strings.ToUpper(blockchain)))
	var MOONSTREAM_IPC_PATH = fmt.Sprintf("http://%s:%s", MOONSTREAM_NODE_IPC_ADDR, MOONSTREAM_NODE_IPC_PORT)

	fmt.Println(MOONSTREAM_IPC_PATH)

	sessionID := uuid.New().String()

	// Humbug crash client to collect errors
	crashReporter, err := humbugClient(sessionID, "moonstream-crawlers", os.Getenv("HUMBUG_REPORTER_CRAWLERS_TOKEN"))
	if err != nil {
		panic(fmt.Sprintf("Invalid Humbug Crash configuration: %s", err.Error()))
	}
	crashReporter.Publish(humbug.SystemReport())

	defer func() {
		message := recover()
		if message != nil {
			fmt.Printf("Error: %s\n", message)
			crashReporter.Publish(humbug.PanicReport(message))
		}
	}()

	// Set connection with Ethereum blockchain via geth
	gethClient, err := rpc.Dial(MOONSTREAM_IPC_PATH)
	if err != nil {
		panic(fmt.Sprintf("Could not connect to geth: %s", err.Error()))
	}
	defer gethClient.Close()

	// Humbug client to be able write data in Bugout journal
	reporter, err := humbugClient(sessionID, os.Getenv("ETHTXPOOL_HUMBUG_CLIENT_ID"), os.Getenv("ETHTXPOOL_HUMBUG_TOKEN"))
	if err != nil {
		panic(fmt.Sprintf("Invalid Humbug configuration: %s", err.Error()))
	}

	PollTxpoolContent(gethClient, intervalSeconds, reporter, blockchain)
}
