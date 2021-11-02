package cmd

import (
	"encoding/json"
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
	query := "SELECT block_number FROM ethereum_blocks ORDER BY block_number DESC LIMIT 1"
	es.db.Raw(query, 1).Scan(&latestBlock.BlockNumber)

	json.NewEncoder(w).Encode(latestBlock)
}
