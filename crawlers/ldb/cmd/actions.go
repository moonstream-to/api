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
func verify(blockchain string, blockNumbers []uint64, workers int) error {
	jobsCh := make(chan Job, workers)
	resultCh := make(chan Result, len(blockNumbers))
	doneCh := make(chan struct{}, workers)

	// Add jobs
	go func() {
		for _, bn := range blockNumbers {
			jobsCh <- Job{
				BlockNumber: bn,
				Results:     resultCh,
			}
		}
		close(jobsCh)
	}()

	for i := 0; i < workers; i++ {
		// Do jobs
		go func() {
			for job := range jobsCh {
				chainBlock, err := localConnections.getChainBlock(job.BlockNumber)
				if err != nil {
					job.Results <- Result{
						ErrorOutput: fmt.Sprintf("Unable to get block: %d from chain, err %v", job.BlockNumber, err),
						ErrorSource: "blockchain",
						Number:      job.BlockNumber,
					}
					continue
				}

				dbBlock, err := localConnections.getDatabaseBlockTxs(blockchain, chainBlock.Hash().String())

				if err != nil {
					job.Results <- Result{
						ErrorOutput: fmt.Sprintf("Unable to get block: %d, err: %v", job.BlockNumber, err),
						ErrorSource: "database",
						Number:      job.BlockNumber,
					}
					continue
				}

				if dbBlock.Number == nil {
					job.Results <- Result{
						ErrorOutput: fmt.Sprintf("Block %d not presented in database", job.BlockNumber),
						ErrorSource: "database",
						Number:      job.BlockNumber,
					}
					continue
				}

				if chainBlock.NumberU64() != dbBlock.Number.Uint64() {
					job.Results <- Result{
						ErrorOutput: fmt.Sprintf("Incorrect %d block retrieved from database", job.BlockNumber),
						ErrorSource: "database",
						Number:      job.BlockNumber,
					}
					continue
				}

				chainTxs := localConnections.getChainTxs(chainBlock.Hash(), job.BlockNumber)

				if len(chainTxs) != len(dbBlock.Transactions) {
					job.Results <- Result{
						ErrorOutput: fmt.Sprintf("Different number of transactions in block %d, err %v", job.BlockNumber, err),
						ErrorSource: "database",
						Number:      job.BlockNumber,
					}
					continue
				}

				job.Results <- Result{
					Output: fmt.Sprintf("Processed block number: %d", job.BlockNumber),
				}
			}
			doneCh <- struct{}{}
		}()
	}

	// Await completion
	go func() {
		for i := 0; i < workers; i++ {
			<-doneCh
		}
		close(resultCh)
	}()

	for result := range resultCh {
		if result.ErrorOutput != "" {
			fmt.Println(result.ErrorOutput)
			corruptBlocks.registerCorruptBlock(result.Number, result.ErrorSource, result.ErrorOutput)
		}
		if result.Output != "" {
			fmt.Println(result.Output)
		}
		if result.Output != "" && result.ErrorOutput != "" {
			fmt.Printf("Unprocessable result with error: %s and output: %s", result.ErrorOutput, result.Output)
		}
	}

	return nil
}
