/*
Main Moonstream crawlers CLI [mooncrawl] handler
*/
package cmd

import (
	"github.com/spf13/cobra"

	mooncrawl "mooncrawl/pkg"
	ethereumcmd "mooncrawl/cmd/ethereum"
	solanacmd "mooncrawl/cmd/solana"
)

var cfgFile string

func GenerateMooncrawlCmd() *cobra.Command {
	mooncrawlCmd := &cobra.Command{
		Use:     "mooncrawl",
		Short:   "Moonstream crawlers commands",
		Long:    `Moonstream crawlers 
CLI for Ethereum and Solana blockchains.`,
		Version: mooncrawl.Version,
	}

	ethereumcmd.PopulateEthereumCommands(mooncrawlCmd)
	solanacmd.PopulateSolanaCommands(mooncrawlCmd)

	return mooncrawlCmd
}

func Execute() {
	mooncrawlCmd := GenerateMooncrawlCmd()
	cobra.CheckErr(mooncrawlCmd.Execute())
}
