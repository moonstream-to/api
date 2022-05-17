package cmd

import (
	"database/sql"
	"fmt"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"

	_ "github.com/lib/pq"
)

var (
	databaseClient DatabaseClient
)

type DatabaseClient struct {
	Client *sql.DB
}

// Establish connection with database
func InitDatabaseClient() error {
	db, err := sql.Open("postgres", configs.MOONSTREAM_DB_URI_READ_ONLY)
	if err != nil {
		return fmt.Errorf("DSN parse error or another database initialization error: %v", err)
	}

	// Set the maximum number of concurrently idle connections,
	// by default sql.DB allows a maximum of 2 idle connections.
	db.SetMaxIdleConns(configs.MOONSTREAM_DB_MAX_IDLE_CONNS)

	// Set the maximum lifetime of a connection.
	// Longer lifetime increase memory usage.
	db.SetConnMaxLifetime(configs.MOONSTREAM_DB_CONN_MAX_LIFETIME)

	databaseClient = DatabaseClient{
		Client: db,
	}

	return nil
}

type Block struct {
	BlockNumber      uint64      `json:"block_number"`
	Difficulty       uint64      `json:"difficulty"`
	ExtraData        string      `json:"extra_data"`
	GasLimit         uint64      `json:"gas_limit"`
	GasUsed          uint64      `json:"gas_used"`
	BaseFeePerGas    interface{} `json:"base_fee_per_gas"`
	Hash             string      `json:"hash"`
	LogsBloom        string      `json:"logs_bloom"`
	Miner            string      `json:"miner"`
	Nonce            string      `json:"nonce"`
	ParentHash       string      `json:"parent_hash"`
	ReceiptRoot      string      `json:"receipt_root"`
	Uncles           string      `json:"uncles"`
	Size             float64     `json:"size"`
	StateRoot        string      `json:"state_root"`
	Timestamp        uint64      `json:"timestamp"`
	TotalDifficulty  string      `json:"total_difficulty"`
	TransactionsRoot string      `json:"transactions_root"`

	IndexedAt string `json:"indexed_at"`
}

// Get block from database
func (dbc *DatabaseClient) GetBlock(blockchain string, blockNumber uint64) (Block, error) {
	var block Block

	// var tableName string
	// if blockchain == "ethereum" {
	// 	tableName = "ethereum_blocks"
	// } else if blockchain == "polygon" {
	// 	tableName = "polygon_blocks"
	// } else {
	// 	return block, fmt.Errorf("Unsupported blockchain")
	// }
	row := dbc.Client.QueryRow(
		"SELECT block_number,difficulty,extra_data,gas_limit,gas_used,base_fee_per_gas,hash,logs_bloom,miner,nonce,parent_hash,receipt_root,uncles,size,state_root,timestamp,total_difficulty,transactions_root,indexed_at FROM ethereum_blocks WHERE block_number = $1",
		// tableName,
		blockNumber,
	)

	if err := row.Scan(
		&block.BlockNumber,
		&block.Difficulty,
		&block.ExtraData,
		&block.GasLimit,
		&block.GasUsed,
		&block.BaseFeePerGas,
		&block.Hash,
		&block.LogsBloom,
		&block.Miner,
		&block.Nonce,
		&block.ParentHash,
		&block.ReceiptRoot,
		&block.Uncles,
		&block.Size,
		&block.StateRoot,
		&block.Timestamp,
		&block.TotalDifficulty,
		&block.TransactionsRoot,
		&block.IndexedAt,
	); err != nil {
		return block, err
	}

	return block, nil
}
