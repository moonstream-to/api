package cmd

import (
	"database/sql"
	"math/big"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/ethereum/go-ethereum/core"
	"github.com/ethereum/go-ethereum/eth/ethconfig"
	"github.com/ethereum/go-ethereum/ethdb"
	"github.com/ethereum/go-ethereum/node"
)

// Modified lightweight go-ethereum struct
// Source: github.com/ethereum/go-ethereum/cmd/geth/config.go
type gethConfig struct {
	Eth  ethconfig.Config
	Node node.Config
}

// Predefined connections to blockchain and database
type LocalConnections struct {
	Stack    *node.Node
	Chain    *core.BlockChain
	ChainDB  ethdb.Database
	Database *sql.DB
}

type HumbugReporter struct {
	Reporter *humbug.HumbugReporter
}

// Lightweight transactions for database operations
type LightTransaction struct {
	Hash string
}

// Lightweight block for database operations
type LightBlock struct {
	Hash         string
	Number       *big.Int
	Transactions []LightTransaction
}

// Malformed block structure which will be submitted to humbug journal
type CorruptBlock struct {
	Number      uint64 `json:"number"`
	Source      string `json:"source"`
	Description string `json:"description"`
}

type CorruptBlocks struct {
	Blocks []CorruptBlock `json:"blocks"`
}

// Concurrency jobs structure
type Job struct {
	BlockNumber uint64
	Results     chan<- Result
}

// TODO(kompotkot): Find way to remove Number, it repeats Job
type Result struct {
	ErrorOutput string
	ErrorSource string
	Number      uint64
	Output      string
}
