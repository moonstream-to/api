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

	var blockLatest BlockLatestResponse
	row := es.db.QueryRow(`SELECT ethereum_blocks.block_number AS ethereum_block_latest,
    polygon_blocks_joinquery.block_number AS polygon_block_latest
FROM ethereum_blocks
    CROSS JOIN (
        SELECT block_number
        FROM polygon_blocks
        ORDER BY block_number DESC
    ) AS polygon_blocks_joinquery
ORDER BY ethereum_blocks.block_number DESC
LIMIT 1`)
	err := row.Scan(&blockLatest.EthereumBlockLatest, &blockLatest.PolygonBlockLatest)
	if err != nil {
		if err == sql.ErrNoRows {
			http.Error(w, "Row not found", http.StatusNotFound)
		} else {
			http.Error(w, "Internal server error", http.StatusInternalServerError)
		}
		log.Printf("An error occurred during sql operation: %s", err)
		return
	}

	json.NewEncoder(w).Encode(blockLatest)
}
