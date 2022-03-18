/*
Ethereum blockchain transaction pool crawler.

Execute:
go run main.go -blockchain ethereum -interval 1
*/
package cmd

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	settings "github.com/bugout-dev/moonstream/crawlers/txpool/configs"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/rpc"
	"github.com/google/uuid"
)

// Generate humbug client
func humbugClient(sessionID string, clientID string, humbugToken string) (*humbug.HumbugReporter, error) {
	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err := humbug.CreateHumbugReporter(consent, clientID, sessionID, humbugToken)
	return reporter, err
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
	currentTransactions := make(map[common.Hash]bool)

	// Structure of the map:
	// {pending | queued} -> "from" address -> nonce -> Transaction
	var result map[string]map[string]map[uint64]*Transaction

	for {
		log.Println("Checking pending transactions in node")
		gethClient.Call(&result, "txpool_content")
		pendingTransactions := result["pending"]

		// Mark all transactions from previous iteration as false
		cacheSizeCounter := 0
		for transactionHash := range currentTransactions {
			currentTransactions[transactionHash] = false
			cacheSizeCounter++
		}
		log.Printf("Size of pending transactions cache at the beginning: %d\n", cacheSizeCounter)

		reports := []humbug.Report{}

		// Iterate over fetched result
		addedTransactionsCounter := 0
		for fromAddress, transactionsByNonce := range pendingTransactions {
			for nonce, transaction := range transactionsByNonce {
				pendingTx := PendingTransaction{From: fromAddress, Nonce: nonce, Transaction: transaction}

				// Check if transaction already exist in our currentTransactions list and pass this transaction
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
						fmt.Sprintf("value:%d", transaction.Value.ToInt()),
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

		// TODO(kompotkot): Passing txs is wrong solution, but for end user
		// it is similar like this txs even not passed through this node.
		if len(reports) < 10000 {
			reportChunks := generateChunks(reports, 500)
			for _, chunk := range reportChunks {
				log.Printf("Published chunk with: %d/%d reports\n", len(chunk), addedTransactionsCounter)
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
			log.Printf("Dropped transactions: %d\n", droppedTransactionsCounter)

			log.Printf("Sleeping for %d seconds\n", interval)
			time.Sleep(time.Duration(interval) * time.Second)
		} else {
			log.Printf("Too many transactions: %d, passing them...\n", addedTransactionsCounter)
		}
	}
}

func InitTxPool() {
	var accessID string
	var blockchain string
	var intervalSeconds int
	flag.StringVar(&accessID, "access-id", "", "Access ID for Moonstream node balancer")
	flag.StringVar(&blockchain, "blockchain", "", "Blockchain to crawl")
	flag.IntVar(&intervalSeconds, "interval", 1, "Number of seconds to wait between RPC calls to query the transaction pool (default: 1)")
	flag.Parse()

	switch blockchain {
	case "ethereum", "polygon":
		log.Printf("%s blockchain\n", strings.Title(blockchain))
	default:
		panic(fmt.Sprintln("Invalid blockchain provided"))
	}

	MOONSTREAM_IPC_PATH := settings.GetIpcPath(blockchain)

	sessionID := uuid.New().String()

	// Humbug crash client to collect errors
	crashReporter, err := humbugClient(sessionID, "moonstream-crawlers", settings.HUMBUG_REPORTER_CRAWLERS_TOKEN)
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
	if accessID != "" {
		gethClient.SetHeader("X-Node-Balancer-Access-Id", accessID)
		gethClient.SetHeader("X-Node-Balancer-Data-Source", "blockchain")
	}
	defer gethClient.Close()

	// Humbug client to be able write data in Bugout journal
	reporter, err := humbugClient(sessionID, settings.HUMBUG_TXPOOL_CLIENT_ID, settings.HUMBUG_TXPOOL_TOKEN)
	if err != nil {
		panic(fmt.Sprintf("Invalid Humbug configuration: %s", err.Error()))
	}

	PollTxpoolContent(gethClient, intervalSeconds, reporter, blockchain)
}
