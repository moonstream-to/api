package cmd

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var (
	stateCLI StateCLI
)

// Command Line Interface state
type StateCLI struct {
	serverCmd  *flag.FlagSet
	clientsCmd *flag.FlagSet

	// Common flags
	showVersion bool

	// Server flags
	listeningAddr     string
	listeningPort     string
	enableHealthCheck bool
	enableDebug       bool
}

func (s *StateCLI) populateCLI() {
	// Subcommands setup
	s.serverCmd = flag.NewFlagSet("server", flag.ExitOnError)
	s.clientsCmd = flag.NewFlagSet("clients", flag.ExitOnError)

	// Server subcommand flag pointers
	s.serverCmd.StringVar(&s.listeningAddr, "host", "127.0.0.1", "Server listening address")
	s.serverCmd.StringVar(&s.listeningPort, "port", "8544", "Server listening port")
	s.serverCmd.BoolVar(&s.enableHealthCheck, "healthcheck", false, "To enable healthcheck ser healthcheck flag")
	s.serverCmd.BoolVar(&s.enableDebug, "debug", false, "To enable debug mode with extended log set debug flag")
}

func init() {
	InitBugoutClient()
}

func CLI() {
	stateCLI.populateCLI()
	if len(os.Args) < 2 {
		fmt.Println("Command: server or version is required")
		os.Exit(1)
	}

	// Parse subcommands and appropriate FlagSet
	switch os.Args[1] {
	case "server":
		stateCLI.serverCmd.Parse(os.Args[2:])
		Server()
	case "clients":
		stateCLI.clientsCmd.Parse(os.Args[2:])
		resources, err := bugoutClient.GetResources(configs.BUGOUT_NODE_BALANCER_CONTROLLER_TOKEN, "")
		if err != nil {
			fmt.Printf("Unable to get resources %v", err)
			return
		}
		resourcesJson, err := json.Marshal(resources)
		if err != nil {
			fmt.Printf("Unable to marshal resources %v", err)
			return
		}
		fmt.Println(string(resourcesJson))
	case "version":
		fmt.Printf("v%s\n", configs.NODE_BALANCER_VERSION)
	default:
		flag.PrintDefaults()
		os.Exit(1)
	}
}
