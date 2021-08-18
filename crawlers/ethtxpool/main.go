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
	From        string            `json:"from"`
	Nonce       uint64            `json:"nonce"`
	Transaction types.Transaction `json:"transaction"`
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

	var result map[string]map[string]map[uint64]*types.Transaction
	gethClient.Call(&result, "txpool_content")
	pendingTransactions := result["pending"]
	for fromAddress, transactionsByNonce := range pendingTransactions {
		for nonce, transaction := range transactionsByNonce {
			pendingTx := PendingTransaction{From: fromAddress, Nonce: nonce, Transaction: *transaction}
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
