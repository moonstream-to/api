package cmd

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var (
	stateCLI StateCLI
)

type flagSlice []string

func (i *flagSlice) String() string {
	return strings.Join(*i, ", ")
}

func (i *flagSlice) Set(value string) error {
	*i = append(*i, value)
	return nil
}

// Command Line Interface state
type StateCLI struct {
	serverCmd  *flag.FlagSet
	versionCmd *flag.FlagSet

	// Common flags
	configPathFlag string
	helpFlag       bool

	// Server flags
	listeningAddrFlag     string
	listeningPortFlag     string
	nodesFlag             flagSlice
	enableHealthCheckFlag bool
	enableDebugFlag       bool
}

func (s *StateCLI) usage() {
	fmt.Printf(`usage: nodebalancer [-h] {%[1]s,%[2]s} ...
Moonstream node balancer CLI
optional arguments:
    -h, --help         show this help message and exit

subcommands:
    {%[1]s,%[2]s}
`, s.serverCmd.Name(), s.versionCmd.Name())
}

func (s *StateCLI) checkRequirements() {
	if s.helpFlag {
		switch {
		case s.serverCmd.Parsed():
			fmt.Printf("Start nodebalancer server\n\n")
			s.serverCmd.PrintDefaults()
			os.Exit(0)
		case s.versionCmd.Parsed():
			fmt.Printf("Show version\n\n")
			s.versionCmd.PrintDefaults()
			os.Exit(0)
		default:
			s.usage()
			os.Exit(0)
		}
	}

	if s.configPathFlag == "" {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			log.Fatalf("Unable to find user home directory, %v", err)
		}

		configDirPath := fmt.Sprintf("%s/.nodebalancer", homeDir)
		configPath := fmt.Sprintf("%s/config.txt", configDirPath)

		err = os.MkdirAll(configDirPath, os.ModePerm)
		if err != nil {
			log.Fatalf("Unable to create directory, %v", err)
		}

		_, err = os.Stat(configPath)
		if err != nil {
			tempConfigB := []byte("ethereum,http://127.0.0.1,8545")
			err = os.WriteFile(configPath, tempConfigB, 0644)
			if err != nil {
				log.Fatalf("Unable to write config, %v", err)
			}
		}

		s.configPathFlag = configPath
	}
}

func (s *StateCLI) populateCLI() {
	// Subcommands setup
	s.serverCmd = flag.NewFlagSet("server", flag.ExitOnError)
	s.versionCmd = flag.NewFlagSet("version", flag.ExitOnError)

	// Common flag pointers
	for _, fs := range []*flag.FlagSet{s.serverCmd, s.versionCmd} {
		fs.BoolVar(&s.helpFlag, "help", false, "Show help message")
		fs.StringVar(&s.configPathFlag, "config", "", "Path to configuration file (default: ~/.nodebalancer/config.txt)")
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

	case "version":
		stateCLI.versionCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		fmt.Printf("v%s\n", configs.NB_VERSION)

	default:
		stateCLI.usage()
		os.Exit(1)
	}
}
