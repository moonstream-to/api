package cmd

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/bugout-dev/moonstream/nodes/node_balancer/configs"

	"github.com/google/uuid"
)

var (
	stateCLI StateCLI
)

// Command Line Interface state
type StateCLI struct {
	addAccessCmd    *flag.FlagSet
	deleteAccessCmd *flag.FlagSet
	serverCmd       *flag.FlagSet
	usersCmd        *flag.FlagSet
	versionCmd      *flag.FlagSet

	// Common flags
	helpFlag bool

	// Add user access flags
	userIDFlag            string
	accessIDFlag          string
	accessNameFlag        string
	accessDescriptionFlag string
	blockchainAccessFlag  bool
	extendedMethodsFlag   bool

	// Server flags
	listeningAddrFlag     string
	listeningPortFlag     string
	enableHealthCheckFlag bool
	enableDebugFlag       bool
}

func (s *StateCLI) usage() {
	fmt.Printf(`usage: nodebalancer [-h] {%[1]s,%[2]s,%[3]s,%[4]s,%[5]s} ...

Moonstream node balancer CLI

optional arguments:
    -h, --help         show this help message and exit

subcommands:
    {%[1]s,%[2]s,%[3]s,%[4]s,%[5]s}
`, s.addAccessCmd.Name(), s.deleteAccessCmd.Name(), s.serverCmd.Name(), s.usersCmd.Name(), s.versionCmd.Name())
}

func (s *StateCLI) checkRequirements() {
	if s.helpFlag {
		switch {
		case s.addAccessCmd.Parsed():
			fmt.Println("add new user access token")
			s.addAccessCmd.PrintDefaults()
			os.Exit(0)
		case s.deleteAccessCmd.Parsed():
			fmt.Println("delete user access token")
			s.deleteAccessCmd.PrintDefaults()
			os.Exit(0)
		case s.serverCmd.Parsed():
			fmt.Println("start nodebalancer server")
			s.serverCmd.PrintDefaults()
			os.Exit(0)
		case s.usersCmd.Parsed():
			fmt.Println("list user access tokens")
			s.usersCmd.PrintDefaults()
			os.Exit(0)
		case s.versionCmd.Parsed():
			fmt.Println("show version")
			s.versionCmd.PrintDefaults()
			os.Exit(0)
		default:
			s.usage()
			os.Exit(0)
		}
	}

	switch {
	case s.addAccessCmd.Parsed():
		if s.userIDFlag == "" {
			fmt.Println("User ID should be specified")
			s.addAccessCmd.PrintDefaults()
			os.Exit(1)
		}
		if s.accessIDFlag == "" {
			s.accessIDFlag = uuid.New().String()
		}
		if s.accessNameFlag == "" {
			fmt.Println("Access name should be specified")
			s.addAccessCmd.PrintDefaults()
			os.Exit(1)
		}
	case s.deleteAccessCmd.Parsed():
		if s.userIDFlag == "" && s.accessIDFlag == "" {
			fmt.Println("User or access ID flag should be specified")
			s.deleteAccessCmd.PrintDefaults()
			os.Exit(1)
		}
	}
}

func (s *StateCLI) populateCLI() {
	// Subcommands setup
	s.addAccessCmd = flag.NewFlagSet("add-access", flag.ExitOnError)
	s.deleteAccessCmd = flag.NewFlagSet("delete-access", flag.ExitOnError)
	s.serverCmd = flag.NewFlagSet("server", flag.ExitOnError)
	s.usersCmd = flag.NewFlagSet("users", flag.ExitOnError)
	s.versionCmd = flag.NewFlagSet("version", flag.ExitOnError)

	// Common flag pointers
	for _, fs := range []*flag.FlagSet{s.addAccessCmd, s.deleteAccessCmd, s.serverCmd, s.usersCmd, s.versionCmd} {
		fs.BoolVar(&s.helpFlag, "help", false, "Show help message")
	}

	// Add, delete and list user access subcommand flag pointers
	for _, fs := range []*flag.FlagSet{s.addAccessCmd, s.deleteAccessCmd, s.usersCmd} {
		fs.StringVar(&s.userIDFlag, "user-id", "", "Bugout user ID")
		fs.StringVar(&s.accessIDFlag, "access-id", "", "UUID for access identification")
	}

	// Add user access subcommand flag pointers
	s.addAccessCmd.StringVar(&s.accessNameFlag, "name", "", "Name of access")
	s.addAccessCmd.StringVar(&s.accessDescriptionFlag, "description", "", "Description of access")
	s.addAccessCmd.BoolVar(&s.blockchainAccessFlag, "blockchain-access", false, "Provide if allow to access blockchain nodes")
	s.addAccessCmd.BoolVar(&s.extendedMethodsFlag, "extended-methods", false, "Provide to be able to execute not whitelisted methods")

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
	case "add-access":
		stateCLI.addAccessCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		proposedUserAccess := UserAccess{
			UserID:           stateCLI.userIDFlag,
			AccessID:         stateCLI.accessIDFlag,
			Name:             stateCLI.accessNameFlag,
			Description:      stateCLI.accessDescriptionFlag,
			BlockchainAccess: stateCLI.blockchainAccessFlag,
			ExtendedMethods:  stateCLI.extendedMethodsFlag,
		}
		userAccess, err := bugoutClient.AddUserAccess(configs.NB_CONTROLLER_TOKEN, proposedUserAccess)
		if err != nil {
			fmt.Printf("Unable to create user access %v\n", err)
			os.Exit(1)
		}
		userAccessJson, err := json.Marshal(userAccess)
		if err != nil {
			fmt.Printf("Unable to marshal user access struct %v\n", err)
			os.Exit(1)
		}
		fmt.Println(string(userAccessJson))

	case "delete-access":
		stateCLI.deleteAccessCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		resources, err := bugoutClient.GetResources(configs.NB_CONTROLLER_TOKEN, stateCLI.userIDFlag, stateCLI.accessIDFlag)
		if err != nil {
			fmt.Printf("Unable to get Bugout resources %v\n", err)
			os.Exit(1)
		}

		var userAccesses []UserAccess
		for _, resource := range resources.Resources {
			deletedResource, err := bugoutClient.DeleteResource(configs.NB_CONTROLLER_TOKEN, resource.ID)
			if err != nil {
				fmt.Printf("Unable to delete resource with id %s %v\n", resource.ID, err)
				continue
			}
			userAccesses = append(userAccesses, deletedResource.ResourceData)
		}

		userAccessesJson, err := json.Marshal(userAccesses)
		if err != nil {
			fmt.Printf("Unable to marshal user access struct %v\n", err)
			os.Exit(1)
		}
		fmt.Println(string(userAccessesJson))

	case "server":
		stateCLI.serverCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		Server()

	case "users":
		stateCLI.usersCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		resources, err := bugoutClient.GetResources(configs.NB_CONTROLLER_TOKEN, stateCLI.userIDFlag, stateCLI.accessIDFlag)
		if err != nil {
			fmt.Printf("Unable to get Bugout resources %v\n", err)
			os.Exit(1)
		}

		var userAccesses []UserAccess
		for _, resourceData := range resources.Resources {
			userAccesses = append(userAccesses, resourceData.ResourceData)
		}
		userAccessesJson, err := json.Marshal(userAccesses)
		if err != nil {
			fmt.Printf("Unable to marshal user accesses struct %v\n", err)
			os.Exit(1)
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
