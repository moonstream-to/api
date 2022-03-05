package cmd

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strconv"

	"github.com/ethereum/go-ethereum/cmd/utils"
	"github.com/google/uuid"
	"gopkg.in/urfave/cli.v1"
)

var (
	BlockchainFlag = cli.StringFlag{
		Name:  "blockchain",
		Usage: `Which blockchain to crawl ("ethereum", "polygon")`,
	}
	DataDirFlag = cli.StringFlag{
		Name:  "datadir",
		Usage: "Data directory for the databases and keystore",
		Value: "/home/ubuntu/nodes/ethereum",
	}
	GCModeFlag = cli.StringFlag{
		Name:  "gcmode",
		Usage: `Blockchain garbage collection mode ("full", "archive")`,
		Value: "full",
	}
)

// Parse start and end blocks from command line input
// TODO(kompotkot): Re-write to work via channel in goroutines
func startEndBlock(ctx *cli.Context) (uint64, uint64, error) {
	start, err := strconv.ParseUint(ctx.Args().Get(0), 10, 32)
	if err != nil {
		return 0, 0, err
	}
	end, err := strconv.ParseUint(ctx.Args().Get(1), 10, 32)
	if err != nil {
		return 0, 0, err
	}

	return start, end, nil
}

func processAddCommand(ctx *cli.Context) error {
	if ctx.NArg() != 2 {
		return fmt.Errorf("Required arguments: %v", ctx.Command.ArgsUsage)
	}
	blockchain := ctx.GlobalString(BlockchainFlag.Name)
	if blockchain != "ethereum" && blockchain != "polygon" {
		return fmt.Errorf("Unsupported blockchain provided")
	}

	start, end, err := startEndBlock(ctx)
	if err != nil {
		return fmt.Errorf("Unable to parse block range: %v", err)
	}

	err = setLocalChain(ctx)
	if err != nil {
		return fmt.Errorf("Unable to set blockchain: %v", err)
	}
	defer localConnections.Stack.Close()
	defer localConnections.ChainDB.Close()

	err = setDatabase()
	if err != nil {
		return fmt.Errorf("Unable to set database connection: %v", err)
	}

	err = add(blockchain, start, end)
	if err != nil {
		return fmt.Errorf("Error occurred due add acction: %v", err)
	}

	localConnections.Chain.Stop()

	return nil
}

func processShowCommand(ctx *cli.Context) error {
	if ctx.NArg() != 2 {
		return fmt.Errorf("Required arguments: %v", ctx.Command.ArgsUsage)
	}
	blockchain := ctx.GlobalString(BlockchainFlag.Name)
	if blockchain != "ethereum" && blockchain != "polygon" {
		return fmt.Errorf("Unsupported blockchain provided")
	}

	start, end, err := startEndBlock(ctx)
	if err != nil {
		return fmt.Errorf("Unable to parse block range: %v", err)
	}

	err = setLocalChain(ctx)
	if err != nil {
		return fmt.Errorf("Unable to set blockchain: %v", err)
	}
	defer localConnections.Stack.Close()
	defer localConnections.ChainDB.Close()

	err = show(start, end)
	if err != nil {
		return fmt.Errorf("Error occurred due show acction: %v", err)
	}

	localConnections.Chain.Stop()

	return nil
}

func processVerifyCommand(ctx *cli.Context) error {
	if ctx.NArg() != 2 {
		return fmt.Errorf("Required arguments: %v", ctx.Command.ArgsUsage)
	}
	blockchain := ctx.GlobalString(BlockchainFlag.Name)
	if blockchain != "ethereum" && blockchain != "polygon" {
		return fmt.Errorf("Unsupported blockchain provided")
	}

	start, end, err := startEndBlock(ctx)
	if err != nil {
		return fmt.Errorf("Unable to parse block range: %v", err)
	}

	err = setLocalChain(ctx)
	if err != nil {
		return fmt.Errorf("Unable to set blockchain: %v", err)
	}
	defer localConnections.Stack.Close()
	defer localConnections.ChainDB.Close()

	err = setDatabase()
	if err != nil {
		return fmt.Errorf("Unable to set database connection: %v", err)
	}

	err = verify(blockchain, start, end)
	if err != nil {
		return fmt.Errorf("Error occurred due verify acction: %v", err)
	}

	localConnections.Chain.Stop()

	return nil
}

func LDBCLI() {
	app := cli.NewApp()
	app.Name = filepath.Base(os.Args[0])
	app.Author = "Bugout.dev"
	app.Email = "engineering@bugout.dev"
	app.Usage = "blockchain ldb extractor command line interface"
	app.Flags = []cli.Flag{
		BlockchainFlag,
		DataDirFlag,
		GCModeFlag,
	}

	app.Commands = []cli.Command{
		{
			Name:        "add",
			Action:      utils.MigrateFlags(processAddCommand),
			ArgsUsage:   "<start_block> <end_block>",
			Usage:       "Add new blocks with transactions to database",
			Description: "This command request blocks from blockchain and adds to database.",
			Flags: []cli.Flag{
				BlockchainFlag,
				DataDirFlag,
				GCModeFlag,
			},
		},
		{
			Name:        "show",
			Action:      utils.MigrateFlags(processShowCommand),
			ArgsUsage:   "<start_block> <end_block>",
			Usage:       "Show block with transactions",
			Description: "This command print out requested blocks.",
			Flags: []cli.Flag{
				BlockchainFlag,
				DataDirFlag,
				GCModeFlag,
			},
		},
		{
			Name:        "verify",
			Action:      utils.MigrateFlags(processVerifyCommand),
			ArgsUsage:   "<start_block> <end_block>",
			Usage:       "Verify blocks with transactions at database",
			Description: "This command compare blocks in database and in blockchain for difference.",
			Flags: []cli.Flag{
				BlockchainFlag,
				DataDirFlag,
				GCModeFlag,
			},
		},
	}

	sort.Sort(cli.FlagsByName(app.Flags))
	sort.Sort(cli.CommandsByName(app.Commands))

	// Initialize local connections
	localConnections = &LocalConnections{}

	// Initialize humbug client to be able write data in Bugout journal
	humbugReporter = &HumbugReporter{}
	sessionID := uuid.New().String()
	err := setHumbugClient(sessionID)
	if err != nil {
		log.Fatal(err)
	}

	err = app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}
