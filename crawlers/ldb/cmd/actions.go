package cmd

import (
	"fmt"

	// "github.com/bugout-dev/moonstream/crawlers/ldb/configs"

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

func add(blockchain string, start, end uint64) error {
	for i := start; i < end; i++ {
		block, err := localConnections.getChainBlock(i)
		if err != nil {
			description := fmt.Sprintf("Unable to get block: %d from chain, err %v", i, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(i, "blockchain", description)
			continue
		}
		td := localConnections.Chain.GetTd(block.Hash(), block.NumberU64())

		chainTxs := localConnections.getChainTxs(block.Hash(), i)

		err = localConnections.writeDatabaseBlockTxs(blockchain, block, chainTxs, td)
		if err != nil {
			fmt.Printf("Error occurred due saving block %d with transactions in database: %v", i, err)
		}

		fmt.Printf("Processed block number: %d\r", i)
	}
	return nil
}

// Return range of block hashes with transaction hashes from blockchain
func show(start, end uint64) error {
	for i := start; i <= end; i++ {
		block, err := localConnections.getChainBlock(i)
		if err != nil {
			fmt.Printf("Unable to get block: %d from chain, err %v\n", i, err)
			continue
		}

		chainTxs := localConnections.getChainTxs(block.Hash(), i)

		var txs []common.Hash
		for _, tx := range chainTxs {
			txs = append(txs, tx.Hash())
		}

		fmt.Printf("Block %d block with hash: %s and transactions: %s\n", block.Number(), block.Hash().String(), txs)
	}

	return nil
}

// Run verification flow of blockchain with database data
func verify(blockchain string, start, end uint64) error {
	var cnt uint64 // Counter until report formed and sent to Humbug

	for i := start; i < end; i++ {
		block, err := localConnections.getChainBlock(i)
		if err != nil {
			description := fmt.Sprintf("Unable to get block: %d from chain, err %v", i, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(i, "blockchain", description)
			continue
		}

		dbBlock, err := localConnections.getDatabaseBlockTxs(blockchain, block.Hash().String())

		if err != nil {
			description := fmt.Sprintf("Unable to get block: %d, err: %v", i, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(i, "database", description)
			continue
		}

		if dbBlock.Number == nil {
			description := fmt.Sprintf("Block %d not presented in database", i)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(i, "database", description)
			continue
		}

		if block.NumberU64() != dbBlock.Number.Uint64() {
			description := fmt.Sprintf("Incorrect %d block retrieved from database", i)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(i, "database", description)
			continue
		}

		chainTxs := localConnections.getChainTxs(block.Hash(), i)

		if len(chainTxs) != len(dbBlock.Transactions) {
			description := fmt.Sprintf("Different number of transactions in block %d, err %v", i, err)
			fmt.Println(description)
			corruptBlocks.registerCorruptBlock(i, "database", description)
			continue
		}

		fmt.Printf("Processed block number: %d\r", i)

		cnt++
		// if cnt >= configs.BLOCK_RANGE_REPORT {
		// 	err := humbugReporter.submitReport(start, end)
		// 	if err != nil {
		// 		return fmt.Errorf("Unable to send humbug report: %v", err)
		// 	}
		// 	cnt = 0
		// }
	}

	// err := humbugReporter.submitReport(start, end)
	// if err != nil {
	// 	return fmt.Errorf("Unable to send humbug report: %v", err)
	// }
	fmt.Println("")

	return nil
}
