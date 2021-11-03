package cmd

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
)

func pingRoute(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

// Fetch latest block record from database
func (es *extendedServer) blocksLatestRoute(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	var latestBlock BlockNumberResponse
	row := es.db.QueryRow("SELECT block_number FROM ethereum_blocks ORDER BY block_number DESC LIMIT 1")
	err := row.Scan(&latestBlock.BlockNumber)
	if err != nil {
		if err == sql.ErrNoRows {
			http.Error(w, "Row not found", http.StatusNotFound)
		} else {
			http.Error(w, "Internal server error", http.StatusInternalServerError)
		}
		log.Printf("An error occurred during sql operation: %s", err)
		return
	}

	json.NewEncoder(w).Encode(latestBlock)
}
