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
	"time"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
	"github.com/google/uuid"
)

var (
	controllerUserAccess UserAccess

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
			log.Printf("Active ethereum clients: %d, polygon clients: %d\n", ethereumClients, polygonClients)
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

	// Configure Humbug reporter to handle errors
	var err error
	sessionID := uuid.New().String()
	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err = humbug.CreateHumbugReporter(consent, "moonstream-node-balancer", sessionID, configs.HUMBUG_REPORTER_NB_TOKEN)
	if err != nil {
		panic(fmt.Sprintf("Invalid Humbug Crash configuration: %s", err.Error()))
	}
	// Record system information
	reporter.Publish(humbug.SystemReport())

	// TODO(kompotkot): Remove, make it work without brood for internal crawlers
	resources, err := bugoutClient.Brood.GetResources(
		configs.NB_CONTROLLER_TOKEN,
		configs.NB_APPLICATION_ID,
		map[string]string{"access_id": configs.NB_CONTROLLER_ACCESS_ID},
	)
	if err != nil {
		fmt.Printf("Unable to get user with provided access identifier %v", err)
	}
	if len(resources.Resources) == 0 {
		fmt.Printf("User with provided access identifier not found %v", err)
	}
	resource_data, err := json.Marshal(resources.Resources[0].ResourceData)
	if err != nil {
		fmt.Printf("Unable to encode resource data interface to json %v", err)
	}
	var userAccess UserAccess
	err = json.Unmarshal(resource_data, &userAccess)
	if err != nil {
		fmt.Printf("Unable to decode resource data json to structure %v", err)
	}
	controllerUserAccess = UserAccess{
		UserID:           userAccess.UserID,
		AccessID:         userAccess.AccessID,
		Name:             userAccess.Name,
		Description:      userAccess.Description,
		BlockchainAccess: userAccess.BlockchainAccess,
		ExtendedMethods:  userAccess.ExtendedMethods,
	}

	err = InitDatabaseClient()
	if err != nil {
		fmt.Printf("Unable to initialize database connection %v", err)
	}

	// Fill NodeConfigList with initial nodes from environment variables
	nodeConfigs.InitNodeConfiguration()

	// Parse nodes and set list of proxies
	for i, nodeConfig := range nodeConfigs.NodeConfigs {
		gethUrl, err := url.Parse(fmt.Sprintf("http://%s:%d", nodeConfig.Addr, nodeConfig.Port))
		if err != nil {
			log.Fatal(err)
		}
		statusUrl, err := url.Parse(fmt.Sprintf("http://%s:%s", nodeConfig.Addr, configs.MOONSTREAM_NODES_SERVER_PORT))
		if err != nil {
			log.Fatal(err)
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
			"Added new %s proxy %d with geth url: %s and status url: %s\n",
			nodeConfig.Blockchain, i, gethUrl, statusUrl)
	}

	serveMux := http.NewServeMux()
	serveMux.Handle("/nb/", accessMiddleware(http.HandlerFunc(lbHandler)))
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

	log.Printf("Starting server at %s:%s\n", stateCLI.listeningAddrFlag, stateCLI.listeningPortFlag)
	err = server.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}
