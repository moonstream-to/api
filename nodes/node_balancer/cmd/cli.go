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
	usersCmd   *flag.FlagSet
	versionCmd *flag.FlagSet

	// Common flags
	helpFlag bool

	// Server flags
	listeningAddrFlag     string
	listeningPortFlag     string
	enableHealthCheckFlag bool
	enableDebugFlag       bool
}

func (s *StateCLI) usage() {
	usage := fmt.Sprintf(`usage: nodebalancer [-h] {%[1]s,%[2]s,%[3]s} ...

Moonstream node balancer CLI

optional arguments:
	-h, --help         show this help message and exit

subcommands:
	{%[1]s,%[2]s,%[3]s}
`, s.serverCmd.Name(), s.usersCmd.Name(), s.versionCmd.Name())

	fmt.Println(usage)
}

func (s *StateCLI) checkRequirements() {
	if s.helpFlag {
		switch {
		case s.serverCmd.Parsed():
			s.serverCmd.PrintDefaults()
		case s.usersCmd.Parsed():
			s.usersCmd.PrintDefaults()
		case s.versionCmd.Parsed():
			s.versionCmd.PrintDefaults()
		default:
			s.usage()
		}
		os.Exit(1)
	}
}

func (s *StateCLI) populateCLI() {
	// Subcommands setup
	s.serverCmd = flag.NewFlagSet("server", flag.ExitOnError)
	s.usersCmd = flag.NewFlagSet("users", flag.ExitOnError)
	s.versionCmd = flag.NewFlagSet("version", flag.ExitOnError)

	// Common flag pointers
	for _, fs := range []*flag.FlagSet{s.serverCmd, s.usersCmd, s.versionCmd} {
		fs.BoolVar(&s.helpFlag, "help", false, "Show help message")
	}

	// Server subcommand flag pointers
	s.serverCmd.StringVar(&s.listeningAddrFlag, "host", "127.0.0.1", "Server listening address")
	s.serverCmd.StringVar(&s.listeningPortFlag, "port", "8544", "Server listening port")
	s.serverCmd.BoolVar(&s.enableHealthCheckFlag, "healthcheck", false, "To enable healthcheck ser healthcheck flag")
	s.serverCmd.BoolVar(&s.enableDebugFlag, "debug", false, "To enable debug mode with extended log set debug flag")
}

func CLI() {
	stateCLI.populateCLI()
	if len(os.Args) < 2 {
		stateCLI.usage()
		os.Exit(1)
	}

	// Parse subcommands and appropriate FlagSet
	switch os.Args[1] {
	case "server":
		stateCLI.serverCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		Server()
	case "users":
		stateCLI.usersCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		userAccesses, err := bugoutClient.GetUserAccesses(configs.NB_CONTROLLER_TOKEN, "", "")
		if err != nil {
			fmt.Printf("Unable to get resources %v", err)
			return
		}
		userAccessesJson, err := json.Marshal(userAccesses)
		if err != nil {
			fmt.Printf("Unable to marshal resources %v", err)
			return
		}
		fmt.Println(string(userAccessesJson))
	case "version":
		stateCLI.versionCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		fmt.Printf("v%s\n", configs.NB_VERSION)
	default:
		stateCLI.usage()
		os.Exit(1)
	}
}

func init() {
	configs.VerifyEnvironments()

	InitBugoutClient()
}
