package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type PingResponse struct {
	Status string `json:"status"`
}

type BlockResponse struct {
	BlockNumber uint64 `json:"block_number"`
}

func ping(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

func blockLatest(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	var latestBlock BlockResponse

	MOONSTREAM_DB_URI := os.Getenv("MOONSTREAM_DB_URI")
	db, err := gorm.Open(postgres.Open(MOONSTREAM_DB_URI), &gorm.Config{})
	if err != nil {
		log.Print(err)
	}

	query := "SELECT block_number FROM ethereum_blocks ORDER BY block_number DESC LIMIT 1"
	db.Raw(query, 1).Scan(&latestBlock.BlockNumber)

	json.NewEncoder(w).Encode(latestBlock)
}

func main() {
	address := "0.0.0.0:8931"
	fmt.Printf("Starting server at %s\n", address)

	http.HandleFunc("/ping", ping)
	http.HandleFunc("/block/latest", blockLatest)

	http.ListenAndServe(address, nil)
}
