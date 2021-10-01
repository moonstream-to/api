package main

import (
	"encoding/json"
	"flag"
	"log"
	"net/http"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var MOONSTREAM_DB_URI = os.Getenv("MOONSTREAM_DB_URI")
var MOONSTREAM_CORS_ALLOWED_ORIGINS = os.Getenv("MOONSTREAM_CORS_ALLOWED_ORIGINS")

type PingResponse struct {
	Status string `json:"status"`
}

type BlockResponse struct {
	BlockNumber uint64 `json:"block_number"`
}

func setupCorsResponse(w *http.ResponseWriter, req *http.Request) {
	(*w).Header().Set("Access-Control-Allow-Origin", MOONSTREAM_CORS_ALLOWED_ORIGINS)
	(*w).Header().Set("Access-Control-Allow-Methods", "GET")
}

func ping(w http.ResponseWriter, req *http.Request) {
	setupCorsResponse(&w, req)
	log.Printf("%s, %s, %q", req.RemoteAddr, req.Method, req.URL.String())
	if (*req).Method == "OPTIONS" {
		return
	}

	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

func blockLatest(w http.ResponseWriter, req *http.Request) {
	setupCorsResponse(&w, req)
	log.Printf("%s, %s, %q", req.RemoteAddr, req.Method, req.URL.String())
	if (*req).Method == "OPTIONS" {
		return
	}

	w.Header().Set("Content-Type", "application/json")

	var latestBlock BlockResponse
	db, err := gorm.Open(postgres.Open(MOONSTREAM_DB_URI), &gorm.Config{})
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}

	query := "SELECT block_number FROM ethereum_blocks ORDER BY block_number DESC LIMIT 1"
	db.Raw(query, 1).Scan(&latestBlock.BlockNumber)

	json.NewEncoder(w).Encode(latestBlock)
}

func main() {
	var listenAddr string
	var listenPort string
	flag.StringVar(&listenAddr, "host", "127.0.0.1", "Server listen address")
	flag.StringVar(&listenPort, "port", "8080", "Server listen port")
	flag.Parse()

	address := listenAddr + ":" + listenPort
	log.Printf("Starting server at %s\n", address)

	http.HandleFunc("/ping", ping)
	http.HandleFunc("/block/latest", blockLatest)

	http.ListenAndServe(address, nil)
}
