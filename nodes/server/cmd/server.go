package cmd

import (
	"flag"
	"log"
	"net/http"
	"time"
)

type extendedServer struct {
	blockchain string
}

func InitServer() {
	var listeningAddr string
	var listeningPort string
	var blockchain string
	flag.StringVar(&listeningAddr, "host", "127.0.0.1", "Server listening address")
	flag.StringVar(&listeningPort, "port", "8080", "Server listening port")
	flag.StringVar(&blockchain, "blockchain", "", "Blockchain to work with (ethereum/polygon/xdai/evmos)")
	flag.Parse()

	es := extendedServer{blockchain: blockchain}

	serverMux := http.NewServeMux()
	serverMux.HandleFunc("/ping", pingRoute)
	serverMux.HandleFunc("/status", es.pingGethRoute)

	// Set middlewares from bottom to top
	serverHandler := corsMiddleware(serverMux)
	serverHandler = logsMiddleware(serverHandler)
	serverHandler = panicMiddleware(serverHandler)

	server := http.Server{
		Addr:         listeningAddr + ":" + listeningPort,
		Handler:      serverHandler,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	log.Printf("Starting server at %s:%s for blockchain %s\n", listeningAddr, listeningPort, blockchain)
	server.ListenAndServe()
}
