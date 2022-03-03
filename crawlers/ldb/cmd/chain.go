package cmd

import (
	"database/sql"
	"fmt"
	"time"

	"github.com/bugout-dev/moonstream/crawlers/ldb/configs"
	_ "github.com/lib/pq"

	"github.com/ethereum/go-ethereum/cmd/utils"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core"
	"github.com/ethereum/go-ethereum/core/rawdb"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/eth/ethconfig"
	"github.com/ethereum/go-ethereum/ethdb"
	"github.com/ethereum/go-ethereum/node"
	"gopkg.in/urfave/cli.v1"
)

type gethConfig struct {
	Eth  ethconfig.Config
	Node node.Config
}

func defaultNodeConfig() node.Config {
	cfg := node.DefaultConfig
	cfg.Name = "geth"
	return cfg
}

type LocalConnections struct {
	Stack    *node.Node
	Chain    *core.BlockChain
	ChainDB  ethdb.Database
	Database *sql.DB
}

func setLocalChain(ctx *cli.Context) error {
	cfg := gethConfig{
		Eth:  ethconfig.Defaults,
		Node: defaultNodeConfig(),
	}

	// Apply flags
	utils.SetNodeConfig(ctx, &cfg.Node)
	stack, err := node.New(&cfg.Node)
	if err != nil {
		return fmt.Errorf("Failed to create the protocol stack: %v", err)
	}
	localConnections.Stack = stack

	utils.SetEthConfig(ctx, stack, &cfg.Eth)

	chain, chainDB := utils.MakeChain(ctx, stack)
	localConnections.Chain = chain
	localConnections.ChainDB = chainDB

	return nil
}

func setDatabase() error {
	db, err := sql.Open("postgres", configs.MOONSTREAM_DB_URI)
	if err != nil {
		return fmt.Errorf("DSN parse error or another database initialization error: %v", err)
	}

	// Set the maximum number of concurrently idle connections,
	// by default sql.DB allows a maximum of 2 idle connections.
	db.SetMaxIdleConns(configs.MOONSTREAM_DB_MAX_IDLE_CONNS)

	// Set the maximum lifetime of a connection.
	// Longer lifetime increase memory usage.
	db.SetConnMaxLifetime(configs.MOONSTREAM_DB_CONN_MAX_LIFETIME)

	localConnections.Database = db

	return nil
}

func (lc *LocalConnections) fetchFromNode(start, end uint64) error {
	for i := start; i <= end; i++ {
		header := lc.Chain.GetHeaderByNumber(i)
		blockHeaderHash := header.Hash()
		body := rawdb.ReadBody(lc.ChainDB, blockHeaderHash, i)
		var txs []common.Hash
		for _, tx := range body.Transactions {
			txs = append(txs, tx.Hash())
		}

		fmt.Printf("- Block header with hash: %s and transactions: %s\n", blockHeaderHash, txs)
	}

	return nil
}

type Block struct {
	Hash        string `json:"hash"`
	BlockNumber uint64 `json:"block_number"`
}

type Transactions struct {
	Txs      []string
	Quantity int
}

// Retrive block from blockchain
func (lc *LocalConnections) getBlockFromChain(number uint64) (*types.Header, error) {
	header := lc.Chain.GetHeaderByNumber(number)
	if header == nil {
		return nil, fmt.Errorf("Not found %d block in chain", number)
	}
	return header, nil
}

// Retrieve block from database
func (lc *LocalConnections) getBlockFromDB(header *types.Header) (Block, error) {
	var block Block
	blockRow := lc.Database.QueryRow(fmt.Sprintf("SELECT hash,block_number FROM ethereum_blocks WHERE hash = '%s';", header.Hash().String()))
	err := blockRow.Scan(&block.Hash, &block.BlockNumber)
	if err != nil {
		if err == sql.ErrNoRows {
			return block, fmt.Errorf("Not found %d block: %v", header.Number, err)
		}
		return block, fmt.Errorf("An error occurred during sql operation: %v", err)
	}

	return block, nil
}

// Retrive block transactions from blockchain
func (lc *LocalConnections) getTxsFromChain(headerHash common.Hash, number uint64) Transactions {
	var transactions Transactions
	body := rawdb.ReadBody(lc.ChainDB, headerHash, number)
	for _, tx := range body.Transactions {
		transactions.Txs = append(transactions.Txs, tx.Hash().String())
		transactions.Quantity++
		// set[tx.Hash().String()] = false
	}

	return transactions
}

// Retrive block transactions from database
func (lc *LocalConnections) getTxsFromDB(blockNumber uint64) (Transactions, error) {
	var transactions Transactions
	rows, err := lc.Database.Query(fmt.Sprintf("SELECT hash FROM ethereum_transactions WHERE block_number = %d;", blockNumber))
	if err != nil {
		return transactions, fmt.Errorf("An error occurred during sql operation: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var txHash string
		err := rows.Scan(&txHash)
		if err != nil {
			return transactions, fmt.Errorf("An error occurred during sql operation: %v", err)
		}
		transactions.Txs = append(transactions.Txs, txHash)
		transactions.Quantity++
		// set[transaction] = true
	}
	return transactions, nil
}

// Write down inconsistent state between database and blockchain
// **source** (string): Source of nonconformity [blockchain, database]
func recordNonconformity(number uint64, source string) {
	fmt.Println(number, source)
}

func verify(start, end uint64) error {
	for i := start; i <= end; i++ {
		header, err := localConnections.getBlockFromChain(i)
		if err != nil {
			fmt.Printf("Unable to get block: %d from chain, err %v\n", i, err)
			recordNonconformity(i, "blockchain")
			continue
		}

		block, err := localConnections.getBlockFromDB(header)
		if err != nil {
			fmt.Printf("Unable to get block: %d, err: %v\n", block.BlockNumber, err)
			recordNonconformity(block.BlockNumber, "database")
			continue
		}

		if header.Number.Uint64() != block.BlockNumber {
			fmt.Printf("Incorrect %d block retrieved from database\n", block.BlockNumber)
			recordNonconformity(block.BlockNumber, "database")
			continue
		}

		// set := make(map[string]bool)
		chainTxs := localConnections.getTxsFromChain(header.Hash(), i)

		dbTxs, err := localConnections.getTxsFromDB(header.Number.Uint64())
		if err != nil {
			fmt.Printf("Unable to get transactions: %d, err: %v\n", block.BlockNumber, err)
			recordNonconformity(block.BlockNumber, "database")
			continue
		}

		if chainTxs.Quantity != dbTxs.Quantity {
			fmt.Printf("Different number of transactions in block %d, err %v\n", block.BlockNumber, err)
			recordNonconformity(block.BlockNumber, "database")
			continue
		}

		fmt.Printf("Processed block number: %d\r", i)
		time.Sleep(1 * time.Second)
	}
	fmt.Println("")

	return nil
}
