/*
Moonstream crawlers CLI for Solana blockchain
[mooncrawl solana] handler
*/
package solanacmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var solanaCmd = &cobra.Command{
	Use:   "sol",
	Short: "Solana crawler commands",
	Long: `Moonstream crawlers CLI for Solana blockchain.

UNDER CONSTRUCTION`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Solana CLI UNDER CONSTRUCTION")
	},
}

func PopulateSolanaCommands(cmd *cobra.Command) {
	cmd.AddCommand(solanaCmd)
}
