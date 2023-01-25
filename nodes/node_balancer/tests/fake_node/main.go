package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"math/rand"
	"time"
	"strconv"
)

type PingResponse struct {
	Status string `json:"status"`
}

// Node status response struct for HealthCheck
type NodeStatusResultResponse struct {
	Number string `json:"number"`
}

type NodeStatusResponse struct {
	Result NodeStatusResultResponse `json:"result"`
}

func pingRoute(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	res := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(res)
}

func lbRoute(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	res := NodeStatusResponse{NodeStatusResultResponse{Number: strconv.Itoa(rand.Intn(100))}}
	json.NewEncoder(w).Encode(res)
}

func logMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		fmt.Printf("[%s] %s %s %s\n", time.Since(start), r.Method, r.URL.Path, r.RemoteAddr)
	})
}

func panicMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				fmt.Println("recovered", err)
				http.Error(w, "Internal server error", 500)
			}
		}()

		next.ServeHTTP(w, r)
	})
}

func main() {
	var listeningAddr string
	var listeningPort string
	flag.StringVar(&listeningAddr, "host", "127.0.0.1", "Server listening address")
	flag.StringVar(&listeningPort, "port", "8545", "Server listening port")
	flag.Parse()

	commonMux := http.NewServeMux()
	commonMux.HandleFunc("/ping", pingRoute)
	commonMux.HandleFunc("/nb/test1/jsonrpc", lbRoute)
	commonMux.HandleFunc("/nb/test2/jsonrpc", lbRoute)

	commonHandler := logMiddleware(commonMux)
	commonHandler = panicMiddleware(commonHandler)

	server := http.Server{
		Addr:         listeningAddr + ":" + listeningPort,
		Handler:      commonHandler,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	log.Printf("Starting server at %s:%s\n", listeningAddr, listeningPort)
	server.ListenAndServe()
}
