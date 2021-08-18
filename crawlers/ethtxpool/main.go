package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/rpc"
	"github.com/google/uuid"
)

func humbugClientFromEnv() (*humbug.HumbugReporter, error) {
	clientID := os.Getenv("ETHTXPOOL_HUMBUG_CLIENT_ID")
	humbugToken := os.Getenv("ETHTXPOOL_HUMBUG_TOKEN")
	sessionID := uuid.New().String()

	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err := humbug.CreateHumbugReporter(consent, clientID, sessionID, humbugToken)
	return reporter, err
}

type PendingTransaction struct {
	From        string      `json:"from"`
	Nonce       uint64      `json:"nonce"`
	Transaction interface{} `json:"transaction"`
}

var ReportTitle string = "Ethereum: Pending transaction"

func main() {
	var gethConnectionString string
	flag.StringVar(&gethConnectionString, "geth", "", "Geth IPC path/RPC url/Websockets URL")
	flag.Parse()

	gethClient, err := rpc.Dial(gethConnectionString)
	if err != nil {
		panic(fmt.Sprintf("Could not connect to geth: %s", err.Error()))
	}

	reporter, err := humbugClientFromEnv()
	if err != nil {
		panic(fmt.Sprintf("Invalid Humbug configuration: %s", err.Error()))
	}

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
	var result map[string]map[string]map[uint64]*types.Transaction
	gethClient.Call(&result, "txpool_content")
	pendingTransactions := result["pending"]
	for fromAddress, transactionsByNonce := range pendingTransactions {
		for nonce, transaction := range transactionsByNonce {
			pendingTx := PendingTransaction{From: fromAddress, Nonce: nonce, Transaction: transaction}
			contents, jsonErr := json.Marshal(pendingTx)
			if jsonErr != nil {
				fmt.Fprintf(os.Stderr, "Error marshalling pending transaction to JSON:\n%v\n", pendingTx)
				continue
			}
			report := humbug.Report{
				Title:   ReportTitle,
				Content: string(contents),
				Tags:    []string{"lol"},
			}
			reporter.Publish(report)
		}
	}
}
