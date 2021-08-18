/*
Moonstream crawlers CLI for Ethereum blockchain
[mooncrawl ethereum] handler
*/
package ethereumcmd

import (
	"github.com/spf13/cobra"
)

func GenerateEthereumCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "eth",
		Short: "Ethereum crawler commands",
		Long:  `Moonstream crawlers CLI for Ethereum blockchain.`,
	}

	return cmd
}

func PopulateEthereumCommands(mooncrawlCmd *cobra.Command) {
	ethCmd := GenerateEthereumCmd()

	ethSyncCmd := GenerateEthereumSyncCmd()
	ethCmd.AddCommand(ethSyncCmd)

	mooncrawlCmd.AddCommand(ethCmd)
}
