/*
Node load balancer API server initialization.
*/
package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"time"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/google/uuid"
)

var (
	internalCrawlersAccess ClientResourceData

	// Crash reporter
	reporter *humbug.HumbugReporter
)

// initHealthCheck runs a routine for check status of the nodes every 5 seconds
func initHealthCheck(debug bool) {
	t := time.NewTicker(configs.NB_HEALTH_CHECK_INTERVAL)
	for {
		select {
		case <-t.C:
			blockchainPool.HealthCheck()
			ethereumClients := ethereumClientPool.CleanInactiveClientNodes()
			polygonClients := polygonClientPool.CleanInactiveClientNodes()
			xdaiClients := xdaiClientPool.CleanInactiveClientNodes()
			log.Printf("Active etehereum clients: %d, polygon clients: %d, xdai clients: %d\n", ethereumClients, polygonClients, xdaiClients)
			if debug {
				blockchainPool.StatusLog()
			}
		}
	}
}

const (
	Attempts int = iota
	Retry
)

// GetAttemptsFromContext returns the attempts for request
func GetAttemptsFromContext(r *http.Request) int {
	if attempts, ok := r.Context().Value(Attempts).(int); ok {
		return attempts
	}
	return 1
}

// GetRetryFromContext returns the retries for request
func GetRetryFromContext(r *http.Request) int {
	if retry, ok := r.Context().Value(Retry).(int); ok {
		return retry
	}
	return 0
}

// Handle errors due calls to proxy endpoint
// Docs: https://pkg.go.dev/net/http/httputil#ReverseProxy
func proxyErrorHandler(proxy *httputil.ReverseProxy, url *url.URL) {
	proxy.ErrorHandler = func(w http.ResponseWriter, r *http.Request, e error) {
		retries := GetRetryFromContext(r)
		if retries < configs.NB_CONNECTION_RETRIES {
			log.Printf(
				"An error occurred while proxying to %s, number of retries: %d/%d. Error: %s\n",
				url, retries+1, configs.NB_CONNECTION_RETRIES, e.Error(),
			)
			select {
			case <-time.After(configs.NB_CONNECTION_RETRIES_INTERVAL):
				ctx := context.WithValue(r.Context(), Retry, retries+1)
				proxy.ServeHTTP(w, r.WithContext(ctx))
			}
			return
		}

		// After 3 retries, mark this backend as down
		blockchainPool.SetNodeStatus(url, false)

		// Set modified path back
		// TODO(kompotkot): Try r.RequestURI instead of header
		r.URL.Path = r.Header.Get("X-Origin-Path")

		// If the same request routing for few attempts with different nodes, increase the count
		// of attempts and send request to next peer
		attempts := GetAttemptsFromContext(r)
		log.Printf("Attempting number: %d to fetch node %s\n", attempts, url)
		ctx := context.WithValue(r.Context(), Attempts, attempts+1)
		lbHandler(w, r.WithContext(ctx))
	}
}

func Server() {
	// Generate map of clients
	CreateClientPools()

	// Create Access ID cache
	CreateAccessCache()

	// Configure Humbug reporter to handle errors
	var err error
	sessionID := uuid.New().String()
	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err = humbug.CreateHumbugReporter(consent, "moonstream-node-balancer", sessionID, configs.HUMBUG_REPORTER_NB_TOKEN)
	if err != nil {
		fmt.Printf("Invalid Humbug Crash configuration: %v", err)
		os.Exit(1)
	}
	// Record system information
	reporter.Publish(humbug.SystemReport())

	resources, err := bugoutClient.Brood.GetResources(
		configs.NB_CONTROLLER_TOKEN,
		configs.NB_APPLICATION_ID,
		map[string]string{"access_id": configs.NB_CONTROLLER_ACCESS_ID},
	)
	if err != nil {
		fmt.Printf("Unable to get user with provided access identifier %v", err)
		os.Exit(1)
	}
	if len(resources.Resources) != 1 {
		fmt.Printf("User with provided access identifier has wrong number of resources %v", err)
		os.Exit(1)
	}
	resource_data, err := json.Marshal(resources.Resources[0].ResourceData)
	if err != nil {
		fmt.Printf("Unable to encode resource data interface to json %v", err)
		os.Exit(1)
	}
	var clientAccess ClientResourceData
	err = json.Unmarshal(resource_data, &clientAccess)
	if err != nil {
		fmt.Printf("Unable to decode resource data json to structure %v", err)
		os.Exit(1)
	}
	internalCrawlersAccess = ClientResourceData{
		UserID:           clientAccess.UserID,
		AccessID:         clientAccess.AccessID,
		Name:             clientAccess.Name,
		Description:      clientAccess.Description,
		BlockchainAccess: clientAccess.BlockchainAccess,
		ExtendedMethods:  clientAccess.ExtendedMethods,
	}
	log.Printf(
		"Internal crawlers access set, resource id: %s, blockchain access: %t, extended methods: %t",
		resources.Resources[0].Id, clientAccess.BlockchainAccess, clientAccess.ExtendedMethods,
	)

	err = InitDatabaseClient()
	if err != nil {
		log.Printf("Unable to initialize database connection %v\n", err)
	} else {
		log.Printf("Connection with database established\n")
	}

	// Fill NodeConfigList with initial nodes from environment variables
	nodeConfigs.InitNodeConfigList(stateCLI.configPathFlag)

	// Parse nodes and set list of proxies
	for i, nodeConfig := range nodeConfigs.NodeConfigs {
		gethUrl, err := url.Parse(fmt.Sprintf("http://%s:%d", nodeConfig.Addr, nodeConfig.Port))
		if err != nil {
			fmt.Printf("Unable to parse gethUrl with addr: %s and port: %d\n", nodeConfig.Addr, nodeConfig.Port)
			continue
		}
		statusUrl, err := url.Parse(fmt.Sprintf("http://%s:%s", nodeConfig.Addr, configs.MOONSTREAM_NODES_SERVER_PORT))
		if err != nil {
			fmt.Printf("Unable to parse statusUrl with addr: %s and port: %s\n", nodeConfig.Addr, configs.MOONSTREAM_NODES_SERVER_PORT)
			continue
		}

		proxyToStatus := httputil.NewSingleHostReverseProxy(statusUrl)
		proxyToGeth := httputil.NewSingleHostReverseProxy(gethUrl)

		proxyErrorHandler(proxyToStatus, statusUrl)
		proxyErrorHandler(proxyToGeth, gethUrl)

		blockchainPool.AddNode(&Node{
			StatusURL:          statusUrl,
			GethURL:            gethUrl,
			Alive:              true,
			StatusReverseProxy: proxyToStatus,
			GethReverseProxy:   proxyToGeth,
		}, nodeConfig.Blockchain)
		log.Printf(
			"Added new %s proxy blockchain under index %d from config file with geth url: %s and status url: %s\n",
			nodeConfig.Blockchain, i, gethUrl, statusUrl)
	}

	serveMux := http.NewServeMux()
	serveMux.Handle("/nb/", accessMiddleware(http.HandlerFunc(lbHandler)))
	log.Println("Authentication middleware enabled")
	if stateCLI.enableDebugFlag {
		serveMux.HandleFunc("/debug", debugRoute)
	}
	serveMux.HandleFunc("/ping", pingRoute)

	// Set common middlewares, from bottom to top
	commonHandler := logMiddleware(serveMux)
	commonHandler = panicMiddleware(commonHandler)

	server := http.Server{
		Addr:         fmt.Sprintf("%s:%s", stateCLI.listeningAddrFlag, stateCLI.listeningPortFlag),
		Handler:      commonHandler,
		ReadTimeout:  40 * time.Second,
		WriteTimeout: 40 * time.Second,
	}

	// Start node health checking and current block fetching
	blockchainPool.HealthCheck()
	if stateCLI.enableHealthCheckFlag {
		go initHealthCheck(stateCLI.enableDebugFlag)
	}

	log.Printf("Starting node load balancer HTTP server at %s:%s\n", stateCLI.listeningAddrFlag, stateCLI.listeningPortFlag)
	err = server.ListenAndServe()
	if err != nil {
		fmt.Printf("Failed to start server listener %v", err)
		os.Exit(1)
	}
}
