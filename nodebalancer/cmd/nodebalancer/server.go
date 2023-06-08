/*
Node load balancer API server initialization.
*/
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strings"
	"time"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/google/uuid"
)

var (
	internalUsageAccess ClientAccess

	// Crash reporter
	reporter *humbug.HumbugReporter
)

// initHealthCheck runs a routine for check status of the nodes every 5 seconds
func initHealthCheck(debug bool) {
	t := time.NewTicker(NB_HEALTH_CHECK_INTERVAL)
	for {
		select {
		case <-t.C:
			blockchainPool.HealthCheck()
			logStr := "Client pool healthcheck."
			for b := range supportedBlockchains {
				cp := clientPool[b]
				clients := cp.CleanInactiveClientNodes()
				logStr += fmt.Sprintf(" Active %s clients: %d.", b, clients)
			}
			log.Println(logStr)
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
		if retries < NB_CONNECTION_RETRIES {
			log.Printf(
				"An error occurred while proxying to %s, number of retries: %d/%d, err: %v",
				url, retries+1, NB_CONNECTION_RETRIES, e.Error(),
			)
			select {
			case <-time.After(NB_CONNECTION_RETRIES_INTERVAL):
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
		log.Printf("Attempting number: %d to fetch node %s", attempts, url)
		ctx := context.WithValue(r.Context(), Attempts, attempts+1)
		lbHandler(w, r.WithContext(ctx))
	}
}

func Server() {
	// Create Access ID cache
	CreateAccessCache()

	// Configure Humbug reporter to handle errors
	var err error
	sessionID := uuid.New().String()
	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err = humbug.CreateHumbugReporter(consent, "moonstream-node-balancer", sessionID, HUMBUG_REPORTER_NB_TOKEN)
	if err != nil {
		fmt.Printf("Invalid Humbug Crash configuration, err: %v\n", err)
		os.Exit(1)
	}
	// Record system information
	reporter.Publish(humbug.SystemReport())

	// Fetch access id for internal usage (crawlers, infrastructure, etc)
	resources, err := bugoutClient.Brood.GetResources(
		NB_CONTROLLER_TOKEN,
		MOONSTREAM_APPLICATION_ID,
		map[string]string{"access_id": NB_CONTROLLER_ACCESS_ID},
	)
	if err != nil {
		fmt.Printf("Unable to get user with provided access identifier, err: %v\n", err)
		os.Exit(1)
	}
	if len(resources.Resources) == 1 {
		resourceData, err := json.Marshal(resources.Resources[0].ResourceData)
		if err != nil {
			fmt.Printf("Unable to encode resource data interface to json, err: %v\n", err)
			os.Exit(1)
		}
		var clientResourceData ClientResourceData
		err = json.Unmarshal(resourceData, &clientResourceData)
		if err != nil {
			fmt.Printf("Unable to decode resource data json to structure, err: %v\n", err)
			os.Exit(1)
		}
		internalUsageAccess = ClientAccess{
			ClientResourceData: ClientResourceData{
				UserID:           clientResourceData.UserID,
				AccessID:         clientResourceData.AccessID,
				Name:             clientResourceData.Name,
				Description:      clientResourceData.Description,
				BlockchainAccess: clientResourceData.BlockchainAccess,
				ExtendedMethods:  clientResourceData.ExtendedMethods,
			},
		}
		log.Printf(
			"Internal crawlers access set, resource id: %s, blockchain access: %t, extended methods: %t",
			resources.Resources[0].Id, clientResourceData.BlockchainAccess, clientResourceData.ExtendedMethods,
		)

	} else if len(resources.Resources) == 0 {
		internalUsageAccess = ClientAccess{
			ClientResourceData: ClientResourceData{
				UserID:           "rnd-user-id",
				AccessID:         NB_CONTROLLER_ACCESS_ID,
				Name:             "rnd-name",
				Description:      "Randomly generated",
				BlockchainAccess: true,
				ExtendedMethods:  true,
			},
		}
		fmt.Printf("There are no provided NB_CONTROLLER_ACCESS_ID records in Brood resources. Using provided with environment variable or randomly generated\n")
	} else {
		fmt.Printf("User with provided access identifier has wrong number of resources: %d\n", len(resources.Resources))
		os.Exit(1)
	}

	// Fill NodeConfigList with initial nodes from environment variables
	err = LoadConfig(stateCLI.configPathFlag)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	supportedBlockchains = make(map[string]bool)

	// Parse nodes and set list of proxies
	for i, nodeConfig := range nodeConfigs {
		endpoint, err := url.Parse(nodeConfig.Endpoint)
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		// Append to supported blockchain set
		supportedBlockchains[nodeConfig.Blockchain] = true

		proxyToEndpoint := httputil.NewSingleHostReverseProxy(endpoint)
		// If required detailed timeout configuration, define node.GethReverseProxy.Transport = &http.Transport{}
		// as modified structure of DefaultTransport net/http/transport/DefaultTransport
		director := proxyToEndpoint.Director
		proxyToEndpoint.Director = func(r *http.Request) {
			director(r)
			// Overwrite Query and Headers to not bypass nodebalancer Query and Headers
			r.URL.RawQuery = ""
			r.Header.Del(strings.Title(NB_ACCESS_ID_HEADER))
			r.Header.Del(strings.Title(NB_DATA_SOURCE_HEADER))
			// Change r.Host from nodebalancer's to end host so TLS check will be passed
			r.Host = r.URL.Host
		}
		proxyErrorHandler(proxyToEndpoint, endpoint)

		blockchainPool.AddNode(&Node{
			Endpoint:         endpoint,
			Alive:            true,
			GethReverseProxy: proxyToEndpoint,
		}, nodeConfig.Blockchain)
		log.Printf(
			"Added new %s proxy blockchain under index %d from config file with geth url: %s://%s",
			nodeConfig.Blockchain, i, endpoint.Scheme, endpoint.Host)
	}

	// Generate map of clients
	CreateClientPools()

	serveMux := http.NewServeMux()
	serveMux.Handle("/nb/", accessMiddleware(http.HandlerFunc(lbHandler)))
	log.Println("Authentication middleware enabled")
	serveMux.HandleFunc("/ping", pingRoute)

	// Set common middlewares, from bottom to top
	commonHandler := corsMiddleware(serveMux)
	commonHandler = logMiddleware(commonHandler)
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

	// Start access id cache cleaning
	go initCacheCleaning(stateCLI.enableDebugFlag)

	log.Printf("Starting node load balancer HTTP server at %s:%s", stateCLI.listeningAddrFlag, stateCLI.listeningPortFlag)
	err = server.ListenAndServe()
	if err != nil {
		fmt.Printf("Failed to start server listener, err: %v\n", err)
		os.Exit(1)
	}
}
