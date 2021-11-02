package cmd

import (
	"database/sql"
	"flag"
	"log"
	"net/http"
)

type extendedServer struct {
	db *sql.DB
}

func InitServer() {
	var listeningAddr string
	var listeningPort string
	flag.StringVar(&listeningAddr, "host", "127.0.0.1", "Server listening address")
	flag.StringVar(&listeningPort, "port", "8080", "Server listening port")
	flag.Parse()

	db := InitDB()
	defer db.Close()

	es := extendedServer{db: db}

	serverMux := http.NewServerMux()
	serverMux.HandleFunc("/ping", pingRoute)
	serverMux.HandleFunc("/block/latest", es.blocksLatestRoute)

	// Set middlewares from bottom to top
	serverHandler := corsMiddleware(serverMux)
	serverHandler = logsMiddleware(serverHandler)
	serverHandler = panicMiddleware(serverHandler)

	server := http.Server{
		Addr:         listeningAddr + ":" + listeningPort,
		Handler:      serverHandler,
		ReadTimeout:  10 * time.Seconds,
		WriteTimeout: 10 * time.Seconds,
	}

	log.Printf("Starting server at %s:%s\n", listeningAddr, listeningPort)
	server.ListenAndServe()
}
