package cmd

import (
	"fmt"

	"github.com/ethereum/go-ethereum/common"
	_ "github.com/lib/pq"
)

var (
	// Block which not found in database or have inconsistencies with blockchain
	corruptBlocks CorruptBlocks
)

// Write down inconsistent state between database and blockchain
/*
- number (uint64): Block number
- source (string): Source of nonconformity [blockchain, database]
- description (string): Description of error, why block marked as malformed
*/
func (cb *CorruptBlocks) registerCorruptBlock(number uint64, source, description string) {
	cb.Blocks = append(cb.Blocks, CorruptBlock{
		Number:      number,
		Source:      source,
		Description: description,
	})
}

// Add new blocks with transactions to database
func add(blockchain string, blockNumbers []uint64) error {
	for _, bn := range blockNumbers {
		block, err := localConnections.getChainBlock(bn)
		if err != nil {
			description := fmt.Sprintf("Unable to get block: %d from chain, err %v", bn, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(bn, "blockchain", description)
			continue
		}
		td := localConnections.Chain.GetTd(block.Hash(), block.NumberU64())

		chainTxs := localConnections.getChainTxs(block.Hash(), bn)

		err = localConnections.writeDatabaseBlockTxs(blockchain, block, chainTxs, td)
		if err != nil {
			fmt.Printf("Error occurred due saving block %d with transactions in database: %v", bn, err)
		}

		fmt.Printf("Processed block number: %d\r", bn)
	}

	return nil
}

// Return range of block hashes with transaction hashes from blockchain
func show(blockNumbers []uint64) error {
	for _, bn := range blockNumbers {
		block, err := localConnections.getChainBlock(bn)
		if err != nil {
			fmt.Printf("Unable to get block: %d from chain, err %v\n", bn, err)
			continue
		}

		chainTxs := localConnections.getChainTxs(block.Hash(), bn)

		var txs []common.Hash
		for _, tx := range chainTxs {
			txs = append(txs, tx.Hash())
		}

		fmt.Printf("Block %d block with hash: %s and transactions: %s\n", block.Number(), block.Hash().String(), txs)
	}

	return nil
}

// Run verification flow of blockchain with database data
func verify(blockchain string, blockNumbers []uint64) error {
	for _, bn := range blockNumbers {
		chainBlock, err := localConnections.getChainBlock(bn)
		if err != nil {
			description := fmt.Sprintf("Unable to get block: %d from chain, err %v", bn, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(bn, "blockchain", description)
			continue
		}

		dbBlock, err := localConnections.getDatabaseBlockTxs(blockchain, chainBlock.Hash().String())

		if err != nil {
			description := fmt.Sprintf("Unable to get block: %d, err: %v", bn, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(bn, "database", description)
			continue
		}

		if dbBlock.Number == nil {
			description := fmt.Sprintf("Block %d not presented in database", bn)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(bn, "database", description)
			continue
		}

		if chainBlock.NumberU64() != dbBlock.Number.Uint64() {
			description := fmt.Sprintf("Incorrect %d block retrieved from database", bn)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(bn, "database", description)
			continue
		}

		chainTxs := localConnections.getChainTxs(chainBlock.Hash(), bn)

		if len(chainTxs) != len(dbBlock.Transactions) {
			description := fmt.Sprintf("Different number of transactions in block %d, err %v", bn, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(bn, "database", description)
			continue
		}

		fmt.Printf("Processed block number: %d\r", bn)
	}

	return nil
}
