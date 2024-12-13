package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	bugout "github.com/bugout-dev/bugout-go/pkg"
	"github.com/google/uuid"
)

var (
	// Storing CLI definitions at server startup
	stateCLI StateCLI

	bugoutClient bugout.BugoutClient

	DEFAULT_ACCESS_NAME          = ""
	DEFAULT_ACCESS_DESCRIPTION   = ""
	DEFAULT_BLOCKCHAIN_ACCESS    = true
	DEFAULT_EXTENDED_METHODS     = true
	DEFAULT_PERIOD_DURATION      = int64(86400) // 1 day
	DEFAULT_MAX_CALLS_PER_PERIOD = int64(10000)
)

// Command Line Interface state
type StateCLI struct {
	addAccessCmd      *flag.FlagSet
	updateAccessCmd   *flag.FlagSet
	generateConfigCmd *flag.FlagSet
	deleteAccessCmd   *flag.FlagSet
	serverCmd         *flag.FlagSet
	usersCmd          *flag.FlagSet
	versionCmd        *flag.FlagSet

	// Common flags
	configPathFlag string
	helpFlag       bool

	// Add/update user access flags
	userIDFlag            string
	accessIDFlag          string
	accessNameFlag        string
	accessDescriptionFlag string

	blockchainAccessFlag bool
	extendedMethodsFlag  bool

	PeriodDurationFlag    int64
	MaxCallsPerPeriodFlag int64

	// Update user access flags
	PeriodStartTsFlag  int64
	CallsPerPeriodFlag int64

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
    {%[1]s,%[2]s,%[3]s,%[4]s,%[5]s,%[6]s,%[7]s}
`, s.addAccessCmd.Name(), s.updateAccessCmd.Name(), s.generateConfigCmd.Name(), s.deleteAccessCmd.Name(), s.serverCmd.Name(), s.usersCmd.Name(), s.versionCmd.Name())
}

// Check if required flags are set
func (s *StateCLI) checkRequirements() {
	if s.helpFlag {
		switch {
		case s.addAccessCmd.Parsed():
			fmt.Printf("Add new user access resource\n\n")
			s.addAccessCmd.PrintDefaults()
			os.Exit(0)
		case s.updateAccessCmd.Parsed():
			fmt.Printf("Update user access resource\n\n")
			s.updateAccessCmd.PrintDefaults()
			os.Exit(0)
		case s.generateConfigCmd.Parsed():
			fmt.Printf("Generate new configuration\n\n")
			s.generateConfigCmd.PrintDefaults()
			os.Exit(0)
		case s.deleteAccessCmd.Parsed():
			fmt.Printf("Delete user access resource\n\n")
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
	case s.updateAccessCmd.Parsed():
		if s.userIDFlag == "" && s.accessIDFlag == "" {
			fmt.Printf("User ID or access ID should be specified\n\n")
			s.updateAccessCmd.PrintDefaults()
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

	// Load configuration
	config, err := GetConfigPath(s.configPathFlag)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	if !config.ConfigExists {
		if err := GenerateDefaultConfig(config); err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
	} else {
		log.Printf("Loaded configuration from %s", config.ConfigPath)
	}
	s.configPathFlag = config.ConfigPath
}

func (s *StateCLI) populateCLI() {
	// Subcommands setup
	s.addAccessCmd = flag.NewFlagSet("add-access", flag.ExitOnError)
	s.updateAccessCmd = flag.NewFlagSet("update-access", flag.ExitOnError)
	s.generateConfigCmd = flag.NewFlagSet("generate-config", flag.ExitOnError)
	s.deleteAccessCmd = flag.NewFlagSet("delete-access", flag.ExitOnError)
	s.serverCmd = flag.NewFlagSet("server", flag.ExitOnError)
	s.usersCmd = flag.NewFlagSet("users", flag.ExitOnError)
	s.versionCmd = flag.NewFlagSet("version", flag.ExitOnError)

	// Common flag pointers
	for _, fs := range []*flag.FlagSet{s.addAccessCmd, s.updateAccessCmd, s.generateConfigCmd, s.deleteAccessCmd, s.serverCmd, s.usersCmd, s.versionCmd} {
		fs.BoolVar(&s.helpFlag, "help", false, "Show help message")
		fs.StringVar(&s.configPathFlag, "config", "", "Path to configuration file (default: ~/.nodebalancer/config.json)")
	}

	// Add, delete and list user access subcommand flag pointers
	for _, fs := range []*flag.FlagSet{s.addAccessCmd, s.updateAccessCmd, s.deleteAccessCmd, s.usersCmd} {
		fs.StringVar(&s.userIDFlag, "user-id", "", "Bugout user ID")
		fs.StringVar(&s.accessIDFlag, "access-id", "", "UUID for access identification")
	}

	// Add/update user access subcommand flag pointers
	for _, fs := range []*flag.FlagSet{s.addAccessCmd, s.updateAccessCmd} {
		fs.StringVar(&s.accessNameFlag, "name", DEFAULT_ACCESS_NAME, fmt.Sprintf("Name of access (default: %s)", DEFAULT_ACCESS_NAME))
		fs.StringVar(&s.accessDescriptionFlag, "description", DEFAULT_ACCESS_DESCRIPTION, fmt.Sprintf("Description of access (default: %s)", DEFAULT_ACCESS_DESCRIPTION))
		fs.BoolVar(&s.blockchainAccessFlag, "blockchain-access", DEFAULT_BLOCKCHAIN_ACCESS, fmt.Sprintf("Specify this flag to grant direct access to blockchain nodes (default: %t)", DEFAULT_BLOCKCHAIN_ACCESS))
		fs.BoolVar(&s.extendedMethodsFlag, "extended-methods", DEFAULT_EXTENDED_METHODS, fmt.Sprintf("Specify this flag to grant execution availability to not whitelisted methods (default: %t)", DEFAULT_EXTENDED_METHODS))
		fs.Int64Var(&s.PeriodDurationFlag, "period-duration", DEFAULT_PERIOD_DURATION, fmt.Sprintf("Access period duration in seconds (default: %d)", DEFAULT_PERIOD_DURATION))
		fs.Int64Var(&s.MaxCallsPerPeriodFlag, "max-calls-per-period", DEFAULT_MAX_CALLS_PER_PERIOD, fmt.Sprintf("Max available calls to node during the period (default: %d)", DEFAULT_MAX_CALLS_PER_PERIOD))
	}

	s.updateAccessCmd.Int64Var(&s.PeriodStartTsFlag, "period-start-ts", 0, "When period starts in unix timestamp format (default: now)")
	s.updateAccessCmd.Int64Var(&s.CallsPerPeriodFlag, "calls-per-period", 0, "Current number of calls to node during the period (default: 0)")

	// Server subcommand flag pointers
	s.serverCmd.StringVar(&s.listeningAddrFlag, "host", "127.0.0.1", "Server listening address")
	s.serverCmd.StringVar(&s.listeningPortFlag, "port", "8544", "Server listening port")
	s.serverCmd.BoolVar(&s.enableHealthCheckFlag, "healthcheck", false, "To enable healthcheck set healthcheck flag")
	s.serverCmd.BoolVar(&s.enableDebugFlag, "debug", false, "To enable debug mode with extended log set debug flag")

	// Users list subcommand flag pointers
	s.usersCmd.IntVar(&s.limitFlag, "limit", 10, "Output result limit")
	s.usersCmd.IntVar(&s.offsetFlag, "offset", 0, "Result output offset")
}

func cli() {
	stateCLI.populateCLI()
	if len(os.Args) < 2 {
		stateCLI.usage()
		os.Exit(1)
	}

	// Init bugout client
	bc, err := CreateBugoutClient()
	if err != nil {
		log.Printf("An error occurred during Bugout client creation: %v", err)
		os.Exit(1)
	}
	bugoutClient = bc

	// Parse subcommands and appropriate FlagSet
	switch os.Args[1] {
	case "generate-config":
		stateCLI.generateConfigCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

	case "add-access":
		stateCLI.addAccessCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		proposedClientResourceData := ClientResourceData{
			UserID:           stateCLI.userIDFlag,
			AccessID:         stateCLI.accessIDFlag,
			Name:             stateCLI.accessNameFlag,
			Description:      stateCLI.accessDescriptionFlag,
			BlockchainAccess: stateCLI.blockchainAccessFlag,
			ExtendedMethods:  stateCLI.extendedMethodsFlag,

			PeriodDuration:    stateCLI.PeriodDurationFlag,
			PeriodStartTs:     time.Now().Unix(),
			MaxCallsPerPeriod: stateCLI.MaxCallsPerPeriodFlag,
			CallsPerPeriod:    0,

			Type: BUGOUT_RESOURCE_TYPE_NODEBALANCER_ACCESS,
		}
		_, err := bugoutClient.Brood.FindUser(
			NB_CONTROLLER_TOKEN,
			map[string]string{
				"user_id":        proposedClientResourceData.UserID,
				"application_id": MOONSTREAM_APPLICATION_ID,
			},
		)
		if err != nil {
			fmt.Printf("User does not exists, err: %v\n", err)
			os.Exit(1)
		}
		resource, err := bugoutClient.Brood.CreateResource(NB_CONTROLLER_TOKEN, MOONSTREAM_APPLICATION_ID, proposedClientResourceData)
		if err != nil {
			fmt.Printf("Unable to create user access, err: %v\n", err)
			os.Exit(1)
		}
		resourceData, err := json.Marshal(resource.ResourceData)
		if err != nil {
			fmt.Printf("Unable to encode resource %s data interface to json, err: %v\n", resource.Id, err)
			os.Exit(1)
		}
		var newUserAccess ClientAccess
		err = json.Unmarshal(resourceData, &newUserAccess)
		if err != nil {
			fmt.Printf("Unable to decode resource %s data json to structure, err: %v\n", resource.Id, err)
			os.Exit(1)
		}
		newUserAccess.ResourceID = resource.Id
		userAccessJson, err := json.Marshal(newUserAccess)
		if err != nil {
			fmt.Printf("Unable to encode resource %s data interface to json, err: %v", resource.Id, err)
			os.Exit(1)
		}
		fmt.Println(string(userAccessJson))

	case "update-access":
		stateCLI.updateAccessCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		queryParameters := make(map[string]string)
		if stateCLI.userIDFlag != "" {
			queryParameters["user_id"] = stateCLI.userIDFlag
		}
		if stateCLI.accessIDFlag != "" {
			queryParameters["access_id"] = stateCLI.accessIDFlag
		}
		resources, err := bugoutClient.Brood.GetResources(
			NB_CONTROLLER_TOKEN,
			MOONSTREAM_APPLICATION_ID,
			queryParameters,
		)
		if err != nil {
			fmt.Printf("Unable to get Bugout resources, err: %v\n", err)
			os.Exit(1)
		}

		resourcesLen := len(resources.Resources)
		if resourcesLen == 0 {
			fmt.Printf("There are no access resource with provided user-id %s or access-id %s\n", stateCLI.userIDFlag, stateCLI.accessIDFlag)
			os.Exit(1)
		}
		if resourcesLen > 1 {
			fmt.Printf("There are several %d access resources with provided user-id %s or access-id %s\n", resourcesLen, stateCLI.userIDFlag, stateCLI.accessIDFlag)
			os.Exit(1)
		}

		resource := resources.Resources[0]
		resourceData, err := json.Marshal(resource.ResourceData)
		if err != nil {
			fmt.Printf("Unable to encode resource %s data interface to json, err: %v\n", resource.Id, err)
			os.Exit(1)
		}

		var currentClientAccess ClientAccess
		currentClientAccess.ResourceID = resource.Id
		err = json.Unmarshal(resourceData, &currentClientAccess.ClientResourceData)
		if err != nil {
			fmt.Printf("Unable to decode resource %s data json to structure, err: %v\n", resource.Id, err)
			os.Exit(1)
		}

		// TODO(kompotkot): Since we are using bool flags I moved with ugly solution.
		// Let's find better one when have free time or will re-write flag Set.
		update := make(map[string]interface{})
		if stateCLI.accessNameFlag != currentClientAccess.ClientResourceData.Name && stateCLI.accessNameFlag != DEFAULT_ACCESS_NAME {
			update["name"] = stateCLI.accessNameFlag
		}
		if stateCLI.accessDescriptionFlag != currentClientAccess.ClientResourceData.Description && stateCLI.accessDescriptionFlag != DEFAULT_ACCESS_DESCRIPTION {
			update["description"] = stateCLI.accessDescriptionFlag
		}
		if stateCLI.blockchainAccessFlag != currentClientAccess.ClientResourceData.BlockchainAccess && stateCLI.blockchainAccessFlag != DEFAULT_BLOCKCHAIN_ACCESS {
			update["blockchain_access"] = stateCLI.blockchainAccessFlag
		}
		if stateCLI.extendedMethodsFlag != currentClientAccess.ClientResourceData.ExtendedMethods && stateCLI.extendedMethodsFlag != DEFAULT_EXTENDED_METHODS {
			update["extended_methods"] = stateCLI.extendedMethodsFlag
		}
		if stateCLI.PeriodDurationFlag != currentClientAccess.ClientResourceData.PeriodDuration && stateCLI.PeriodDurationFlag != DEFAULT_PERIOD_DURATION {
			update["period_duration"] = stateCLI.PeriodDurationFlag
		}
		if stateCLI.MaxCallsPerPeriodFlag != currentClientAccess.ClientResourceData.MaxCallsPerPeriod && stateCLI.MaxCallsPerPeriodFlag != DEFAULT_MAX_CALLS_PER_PERIOD {
			update["max_calls_per_period"] = stateCLI.MaxCallsPerPeriodFlag
		}
		if stateCLI.PeriodStartTsFlag != currentClientAccess.ClientResourceData.PeriodStartTs && stateCLI.PeriodStartTsFlag != 0 {
			update["period_start_ts"] = stateCLI.PeriodStartTsFlag
		}
		if stateCLI.CallsPerPeriodFlag != currentClientAccess.ClientResourceData.CallsPerPeriod && stateCLI.CallsPerPeriodFlag != 0 {
			update["calls_per_period"] = stateCLI.CallsPerPeriodFlag
		}

		updatedResource, err := bugoutClient.Brood.UpdateResource(
			NB_CONTROLLER_TOKEN,
			resource.Id,
			update,
			[]string{},
		)
		if err != nil {
			fmt.Printf("Unable to update Bugout resource, err: %v\n", err)
			os.Exit(1)
		}

		updatedResourceData, err := json.Marshal(updatedResource.ResourceData)
		if err != nil {
			fmt.Printf("Unable to encode resource %s data interface to json, err: %v\n", resource.Id, err)
			os.Exit(1)
		}
		var updatedUserAccess ClientAccess
		err = json.Unmarshal(updatedResourceData, &updatedUserAccess)
		if err != nil {
			fmt.Printf("Unable to decode resource %s data json to structure, err: %v\n", resource.Id, err)
			os.Exit(1)
		}
		updatedUserAccess.ResourceID = updatedResource.Id
		userAccessJson, err := json.Marshal(updatedUserAccess)
		if err != nil {
			fmt.Printf("Unable to marshal user access struct, err: %v\n", err)
			os.Exit(1)
		}
		fmt.Println(string(userAccessJson))

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
			NB_CONTROLLER_TOKEN,
			MOONSTREAM_APPLICATION_ID,
			queryParameters,
		)
		if err != nil {
			fmt.Printf("Unable to get Bugout resources, err: %v\n", err)
			os.Exit(1)
		}

		var userAccesses []ClientAccess
		for _, resource := range resources.Resources {
			deletedResource, err := bugoutClient.Brood.DeleteResource(NB_CONTROLLER_TOKEN, resource.Id)
			if err != nil {
				fmt.Printf("Unable to delete resource %s, err: %v\n", resource.Id, err)
				continue
			}
			deletedResourceData, err := json.Marshal(deletedResource.ResourceData)
			if err != nil {
				fmt.Printf("Unable to encode resource %s data interface to json, err: %v\n", resource.Id, err)
				continue
			}
			var deletedUserAccess ClientAccess
			err = json.Unmarshal(deletedResourceData, &deletedUserAccess)
			if err != nil {
				fmt.Printf("Unable to decode resource %s data json to structure, err: %v\n", resource.Id, err)
				continue
			}
			deletedUserAccess.ResourceID = deletedResource.Id
			userAccesses = append(userAccesses, deletedUserAccess)
		}

		userAccessesJson, err := json.Marshal(userAccesses)
		if err != nil {
			fmt.Printf("Unable to marshal user access struct, err: %v\n", err)
			os.Exit(1)
		}
		fmt.Println(string(userAccessesJson))

	case "server":
		stateCLI.serverCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		CheckEnvVarSet()

		Server()

	case "users":
		stateCLI.usersCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		queryParameters := make(map[string]string)
		if stateCLI.userIDFlag != "" {
			queryParameters["user_id"] = stateCLI.userIDFlag
		}
		if stateCLI.accessIDFlag != "" {
			queryParameters["access_id"] = stateCLI.accessIDFlag
		}
		resources, err := bugoutClient.Brood.GetResources(
			NB_CONTROLLER_TOKEN,
			MOONSTREAM_APPLICATION_ID,
			queryParameters,
		)
		if err != nil {
			fmt.Printf("Unable to get Bugout resources, err: %v\n", err)
			os.Exit(1)
		}

		var clientAccesses []ClientAccess

		offset := stateCLI.offsetFlag
		if stateCLI.offsetFlag > len(resources.Resources) {
			offset = len(resources.Resources)
		}
		limit := stateCLI.offsetFlag + stateCLI.limitFlag
		if limit > len(resources.Resources) {
			limit = len(resources.Resources[offset:]) + offset
		}

		for _, resource := range resources.Resources[offset:limit] {
			resourceData, err := json.Marshal(resource.ResourceData)
			if err != nil {
				fmt.Printf("Unable to encode resource %s data interface to json, err: %v\n", resource.Id, err)
				continue
			}
			var clientAccess ClientAccess
			clientAccess.ResourceID = resource.Id
			err = json.Unmarshal(resourceData, &clientAccess.ClientResourceData)
			if err != nil {
				fmt.Printf("Unable to decode resource %s data json to structure, err: %v\n", resource.Id, err)
				continue
			}
			clientAccesses = append(clientAccesses, clientAccess)
		}
		userAccessesJson, err := json.Marshal(clientAccesses)
		if err != nil {
			fmt.Printf("Unable to marshal user accesses struct, err: %v\n", err)
			os.Exit(1)
		}
		fmt.Println(string(userAccessesJson))

	case "version":
		stateCLI.versionCmd.Parse(os.Args[2:])
		stateCLI.checkRequirements()

		fmt.Printf("v%s\n", NB_VERSION)

	default:
		stateCLI.usage()
		os.Exit(1)
	}
}
