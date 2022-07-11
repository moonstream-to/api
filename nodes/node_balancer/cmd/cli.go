package cmd

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"

	bugout "github.com/bugout-dev/bugout-go/pkg"
	"github.com/google/uuid"

	"github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var (
	// Storing CLI definitions at server startup
	stateCLI StateCLI

	bugoutClient bugout.BugoutClient
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
	addAccessCmd      *flag.FlagSet
	generateConfigCmd *flag.FlagSet
	deleteAccessCmd   *flag.FlagSet
	serverCmd         *flag.FlagSet
	usersCmd          *flag.FlagSet
	versionCmd        *flag.FlagSet

	// Common flags
	configPathFlag string
	helpFlag       bool

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

	// Users list flags
	limitFlag  int
	offsetFlag int
}

func (s *StateCLI) usage() {
	fmt.Printf(`usage: nodebalancer [-h] {%[1]s,%[2]s,%[3]s,%[4]s,%[5]s,%[6]s} ...

Moonstream node balancer CLI
optional arguments:
    -h, --help         show this help message and exit

subcommands:
    {%[1]s,%[2]s,%[3]s,%[4]s,%[5]s,%[6]s}
`, s.addAccessCmd.Name(), s.generateConfigCmd.Name(), s.deleteAccessCmd.Name(), s.serverCmd.Name(), s.usersCmd.Name(), s.versionCmd.Name())
}

// Check if required flags are set
func (s *StateCLI) checkRequirements() {
	if s.helpFlag {
		switch {
		case s.addAccessCmd.Parsed():
			fmt.Printf("Add new user access token\n\n")
			s.addAccessCmd.PrintDefaults()
			os.Exit(0)
		case s.generateConfigCmd.Parsed():
			fmt.Printf("Generate new configuration\n\n")
			s.generateConfigCmd.PrintDefaults()
			os.Exit(0)
		case s.deleteAccessCmd.Parsed():
			fmt.Printf("Delete user access token\n\n")
			s.deleteAccessCmd.PrintDefaults()
			os.Exit(0)
		case s.serverCmd.Parsed():
			fmt.Printf("Start nodebalancer server\n\n")
			s.serverCmd.PrintDefaults()
			os.Exit(0)
		case s.usersCmd.Parsed():
			fmt.Printf("List user access tokens\n\n")
			s.usersCmd.PrintDefaults()
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

	switch {
	case s.addAccessCmd.Parsed():
		if s.userIDFlag == "" {
			fmt.Printf("User ID should be specified\n\n")
			s.addAccessCmd.PrintDefaults()
			os.Exit(1)
		}
		if s.accessIDFlag == "" {
			s.accessIDFlag = uuid.New().String()
		}
		if s.accessNameFlag == "" {
			fmt.Printf("Access name should be specified\n\n")
			s.addAccessCmd.PrintDefaults()
			os.Exit(1)
		}
	case s.deleteAccessCmd.Parsed():
		if s.userIDFlag == "" && s.accessIDFlag == "" {
			fmt.Printf("User or access ID flag should be specified\n\n")
			s.deleteAccessCmd.PrintDefaults()
			os.Exit(1)
		}
	case s.usersCmd.Parsed():
		if s.offsetFlag < 0 || s.limitFlag < 0 {
			fmt.Printf("Offset and limit flags should be greater then zero\n\n")
			s.usersCmd.PrintDefaults()
			os.Exit(1)
		}
	}

	config := configs.GetConfigPath(s.configPathFlag)
	fmt.Println(config)
	if !configs.CheckPathExists(config.ConfigPath) {
		configs.GenerateDefaultConfig(config)
	}
	s.configPathFlag = config.ConfigPath
}

func (s *StateCLI) populateCLI() {
	// Subcommands setup
	s.addAccessCmd = flag.NewFlagSet("add-access", flag.ExitOnError)
	s.generateConfigCmd = flag.NewFlagSet("generate-config", flag.ExitOnError)
	s.deleteAccessCmd = flag.NewFlagSet("delete-access", flag.ExitOnError)
	s.serverCmd = flag.NewFlagSet("server", flag.ExitOnError)
	s.usersCmd = flag.NewFlagSet("users", flag.ExitOnError)
	s.versionCmd = flag.NewFlagSet("version", flag.ExitOnError)

	// Common flag pointers
	for _, fs := range []*flag.FlagSet{s.addAccessCmd, s.generateConfigCmd, s.deleteAccessCmd, s.serverCmd, s.usersCmd, s.versionCmd} {
		fs.BoolVar(&s.helpFlag, "help", false, "Show help message")
		fs.StringVar(&s.configPathFlag, "config", "", "Path to configuration file (default: ~/.nodebalancer/config.txt)")
	}

	// Add, delete and list user access subcommand flag pointers
	for _, fs := range []*flag.FlagSet{s.addAccessCmd, s.deleteAccessCmd, s.usersCmd} {
		fs.StringVar(&s.userIDFlag, "user-id", "", "Bugout user ID")
		fs.StringVar(&s.accessIDFlag, "access-id", "", "UUID for access identification")
	}

	// Add user access subcommand flag pointers
	s.addAccessCmd.StringVar(&s.accessNameFlag, "name", "", "Name of access")
	s.addAccessCmd.StringVar(&s.accessDescriptionFlag, "description", "", "Description of access")
	s.addAccessCmd.BoolVar(&s.blockchainAccessFlag, "blockchain-access", false, "Provide if allow direct access to blockchain nodes")
	s.addAccessCmd.BoolVar(&s.extendedMethodsFlag, "extended-methods", false, "Provide to be able to execute not whitelisted methods")

	// Server subcommand flag pointers
	s.serverCmd.StringVar(&s.listeningAddrFlag, "host", "127.0.0.1", "Server listening address")
	s.serverCmd.StringVar(&s.listeningPortFlag, "port", "8544", "Server listening port")
	s.serverCmd.BoolVar(&s.enableHealthCheckFlag, "healthcheck", false, "To enable healthcheck set healthcheck flag")
	s.serverCmd.BoolVar(&s.enableDebugFlag, "debug", false, "To enable debug mode with extended log set debug flag")

	// Users list subcommand flag pointers
	s.usersCmd.IntVar(&s.limitFlag, "limit", 10, "Output result limit")
	s.usersCmd.IntVar(&s.offsetFlag, "offset", 0, "Result output offset")
}

func CLI() {
	stateCLI.populateCLI()
	if len(os.Args) < 2 {
		stateCLI.usage()
		os.Exit(1)
	}

	// Init bugout client
	bc, err := bugout.ClientFromEnv()
	if err != nil {
		fmt.Printf("Unable to initialize bugout client %v", err)
		os.Exit(1)
	}
	bugoutClient = bc

	// Parse subcommands and appropriate FlagSet
	switch os.Args[1] {
	case "add-access":
		stateCLI.addAccessCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		proposedUserAccess := ClientResourceData{
			UserID:           stateCLI.userIDFlag,
			AccessID:         stateCLI.accessIDFlag,
			Name:             stateCLI.accessNameFlag,
			Description:      stateCLI.accessDescriptionFlag,
			BlockchainAccess: stateCLI.blockchainAccessFlag,
			ExtendedMethods:  stateCLI.extendedMethodsFlag,
		}
		_, err := bugoutClient.Brood.FindUser(
			configs.NB_CONTROLLER_TOKEN,
			map[string]string{
				"user_id":        proposedUserAccess.UserID,
				"application_id": configs.NB_APPLICATION_ID,
			},
		)
		if err != nil {
			fmt.Printf("User does not exists %v\n", err)
			os.Exit(1)
		}
		resource, err := bugoutClient.Brood.CreateResource(configs.NB_CONTROLLER_TOKEN, configs.NB_APPLICATION_ID, proposedUserAccess)
		if err != nil {
			fmt.Printf("Unable to create user access %v\n", err)
			os.Exit(1)
		}
		resource_data, err := json.Marshal(resource.ResourceData)
		if err != nil {
			fmt.Printf("Unable to encode resource %s data interface to json %v", resource.Id, err)
			os.Exit(1)
		}
		fmt.Println(string(resource_data))

	case "generate-config":
		stateCLI.generateConfigCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

	case "delete-access":
		stateCLI.deleteAccessCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		queryParameters := make(map[string]string)
		if stateCLI.userIDFlag != "" {
			queryParameters["user_id"] = stateCLI.userIDFlag
		}
		if stateCLI.accessIDFlag != "" {
			queryParameters["access_id"] = stateCLI.accessIDFlag
		}
		resources, err := bugoutClient.Brood.GetResources(
			configs.NB_CONTROLLER_TOKEN,
			configs.NB_APPLICATION_ID,
			queryParameters,
		)
		if err != nil {
			fmt.Printf("Unable to get Bugout resources %v\n", err)
			os.Exit(1)
		}

		var userAccesses []ClientResourceData
		for _, resource := range resources.Resources {
			deletedResource, err := bugoutClient.Brood.DeleteResource(configs.NB_CONTROLLER_TOKEN, resource.Id)
			if err != nil {
				fmt.Printf("Unable to delete resource %s %v\n", resource.Id, err)
				continue
			}
			resource_data, err := json.Marshal(deletedResource.ResourceData)
			if err != nil {
				fmt.Printf("Unable to encode resource %s data interface to json %v", resource.Id, err)
				continue
			}
			var userAccess ClientResourceData
			err = json.Unmarshal(resource_data, &userAccess)
			if err != nil {
				fmt.Printf("Unable to decode resource %s data json to structure %v", resource.Id, err)
				continue
			}
			userAccesses = append(userAccesses, userAccess)
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

		configs.CheckEnvVarSet()

		Server()

	case "users":
		stateCLI.usersCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		var queryParameters map[string]string
		if stateCLI.userIDFlag != "" {
			queryParameters["user_id"] = stateCLI.userIDFlag
		}
		if stateCLI.accessIDFlag != "" {
			queryParameters["access_id"] = stateCLI.accessIDFlag
		}
		resources, err := bugoutClient.Brood.GetResources(
			configs.NB_CONTROLLER_TOKEN,
			configs.NB_APPLICATION_ID,
			queryParameters,
		)
		if err != nil {
			fmt.Printf("Unable to get Bugout resources %v\n", err)
			os.Exit(1)
		}

		var userAccesses []ClientResourceData

		offset := stateCLI.offsetFlag
		if stateCLI.offsetFlag > len(resources.Resources) {
			offset = len(resources.Resources)
		}
		limit := stateCLI.offsetFlag + stateCLI.limitFlag
		if limit > len(resources.Resources) {
			limit = len(resources.Resources[offset:]) + offset
		}

		for _, resource := range resources.Resources[offset:limit] {
			resource_data, err := json.Marshal(resource.ResourceData)
			if err != nil {
				fmt.Printf("Unable to encode resource %s data interface to json %v", resource.Id, err)
				continue
			}
			var userAccess ClientResourceData
			err = json.Unmarshal(resource_data, &userAccess)
			if err != nil {
				fmt.Printf("Unable to decode resource %s data json to structure %v", resource.Id, err)
				continue
			}
			userAccesses = append(userAccesses, userAccess)
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
