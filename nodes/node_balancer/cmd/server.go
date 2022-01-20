/*
Node load balancer API server initialization.
*/
package cmd

import (
	"context"
	"flag"
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

var reporter *humbug.HumbugReporter

// initHealthCheck runs a routine for check status of the nodes every 5 seconds
func initHealthCheck(debug bool) {
	t := time.NewTicker(configs.NB_HEALTH_CHECK_INTERVAL)
	for {
		select {
		case <-t.C:
			blockchainPool.HealthCheck()
			ethereumClients := ethereumClientPool.CleanInactiveClientNodes()
			polygonClients := polygonClientPool.CleanInactiveClientNodes()
			log.Printf("Active etehereum clients: %d, polygon clients: %d\n", ethereumClients, polygonClients)
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

func InitServer() {
	var listeningAddr string
	var listeningPort string
	var enableHealthCheck bool
	var enableDebug bool
	var showVersion bool
	flag.StringVar(&listeningAddr, "host", "127.0.0.1", "Server listening address")
	flag.StringVar(&listeningPort, "port", "8544", "Server listening port")
	flag.BoolVar(&enableHealthCheck, "healthcheck", false, "To enable healthcheck ser healthcheck flag")
	flag.BoolVar(&enableDebug, "debug", false, "To enable debug mode with extended log set debug flag")
	flag.BoolVar(&showVersion, "version", false, "Print version")
	flag.Parse()

	if showVersion {
		fmt.Printf("Node balancer version: v%s\n", configs.NODE_BALANCER_VERSION)
		return
	}

	// Generate map of clients
	CreateClientPools()

	// Configure Humbug reporter to handle errors
	var err error
	sessionID := uuid.New().String()
	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err = humbug.CreateHumbugReporter(consent, "moonstream-node-balancer", sessionID, configs.HUMBUG_REPORTER_NODE_BALANCER_TOKEN)
	if err != nil {
		panic(fmt.Sprintf("Invalid Humbug Crash configuration: %s", err.Error()))
	}
	// Record system information
	reporter.Publish(humbug.SystemReport())

	// Fill NodeConfigList with initial nodes from environment variables
	configs.ConfigList.InitNodeConfigList()

	// Parse nodes and set list of proxies
	for i, nodeConfig := range configs.ConfigList.Configs {
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
	serveMux.HandleFunc("/ping", pingRoute)
	serveMux.HandleFunc("/nb/", lbHandler)

	// Set common middlewares, from bottom to top
	commonHandler := logMiddleware(serveMux)
	commonHandler = panicMiddleware(commonHandler)

	server := http.Server{
		Addr:         fmt.Sprintf("%s:%s", listeningAddr, listeningPort),
		Handler:      commonHandler,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	// Start node health checking and current block fetching
	if enableHealthCheck {
		go initHealthCheck(enableDebug)
	}

	log.Printf("Starting server at %s:%s\n", listeningAddr, listeningPort)
	err = server.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}
