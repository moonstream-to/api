package ethereumcmd

import (
	// "fmt"

	"github.com/spf13/cobra"
	mooncrawl "mooncrawl/pkg"
)

func GenerateEthereumSyncCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "sync",
		Short: "Ethereum synchronization commands",
		Long:  `Moonstream crawlers CLI for synchronization with Ethereum blockchain.`,
	}

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	cmd.PersistentFlags().String("ipc_path", "", "IPC/HTTP path of Ethereum blockchain")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// cmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")

	txpoolCmd := GenerateEthereumSyncTxpoolCmd()
	cmd.AddCommand(txpoolCmd)

	return cmd
}

func GenerateEthereumSyncTxpoolCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "txpool",
		Short: "Ethereum txpool commands",
		Long: `Moonstream crawlers CLI for transactions pool 
of Ethereum blockchain.`,
		Run: func(cmd *cobra.Command, args []string) {
			mooncrawl.Client()
			// client, err := mooncrawl.Client()
			
			// if err != nil {
			// 	fmt.Println(err)
			// 	return
			// }

			// mooncrawl.PrBlock(client)
		},
	}

	return cmd
}
