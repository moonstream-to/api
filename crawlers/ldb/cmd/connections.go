package cmd

import (
	"database/sql"
	"fmt"
	"math/big"

	"github.com/bugout-dev/moonstream/crawlers/ldb/configs"

	"github.com/ethereum/go-ethereum/cmd/utils"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/rawdb"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/eth/ethconfig"
	"github.com/ethereum/go-ethereum/node"
	_ "github.com/lib/pq"
	"gopkg.in/urfave/cli.v1"
)

var (
	localConnections *LocalConnections
)

// Modified lightweight go-ethereum function
// Source: github.com/ethereum/go-ethereum/cmd/geth/config.go
func defaultNodeConfig() node.Config {
	cfg := node.DefaultConfig
	cfg.Name = "geth"
	return cfg
}

// Establish connection with blockchain
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

// Establish connection with database
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

// Retrive block from blockchain
func (lc *LocalConnections) getChainBlock(number uint64) (*types.Header, error) {
	header := lc.Chain.GetHeaderByNumber(number)
	if header == nil {
		return nil, fmt.Errorf("Not found %d block in chain", number)
	}
	return header, nil
}

// Retrive block transactions from blockchain
func (lc *LocalConnections) getChainTxs(headerHash common.Hash, number uint64) []*types.Transaction {
	var transactions []*types.Transaction
	body := rawdb.ReadBody(lc.ChainDB, headerHash, number)
	for _, tx := range body.Transactions {
		transactions = append(transactions, tx)
	}

	return transactions
}

// Retrive block with transactions from database
func (lc *LocalConnections) getDatabaseBlockTxs(blockchain, headerHash string) (LightBlock, error) {
	var lBlock LightBlock
	var txs []LightTransaction
	query := fmt.Sprintf(
		`SELECT 
			%s_blocks.hash,
			%s_blocks.block_number,
			%s_transactions.hash
		FROM %s_blocks
			LEFT JOIN %s_transactions ON %s_blocks.block_number = %s_transactions.block_number
		WHERE %s_blocks.hash = '%s';`,
		blockchain,
		blockchain,
		blockchain,
		blockchain,
		blockchain,
		blockchain,
		blockchain,
		blockchain,
		headerHash,
	)
	rows, err := lc.Database.Query(query)
	if err != nil {
		return lBlock, fmt.Errorf("An error occurred during sql operation: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var blockHash, blockNumberStr, txHash sql.NullString
		err := rows.Scan(&blockHash, &blockNumberStr, &txHash)
		if err != nil {
			return lBlock, fmt.Errorf("An error occurred during sql operation: %v", err)
		}

		var lTx LightTransaction
		if txHash.Valid != false {
			lTx = LightTransaction{
				Hash: txHash.String,
			}
			txs = append(lBlock.Transactions, lTx)
		}

		blockNumber := new(big.Int)
		blockNumber, ok := blockNumber.SetString(blockNumberStr.String, 10)
		if !ok {
			return lBlock, fmt.Errorf("Unable to parse block number")
		}

		lBlock = LightBlock{
			Hash:         blockHash.String,
			Number:       blockNumber,
			Transactions: txs,
		}
	}

	return lBlock, nil
}
