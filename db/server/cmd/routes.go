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

	var blockNumbers []uint64
	var blockLatest BlockLatestResponse
	rows, err := es.db.Query(`(SELECT block_number FROM ethereum_blocks ORDER BY block_number DESC LIMIT 1)
	UNION ALL
	(SELECT block_number FROM polygon_blocks ORDER BY block_number DESC LIMIT 1)
	UNION ALL
	(SELECT block_number FROM polygon_labels WHERE label = 'moonworm-alpha' ORDER BY block_number DESC LIMIT 1)`)
	if err != nil {
		log.Printf("An error occurred during sql operation: %s", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	for rows.Next() {
		var bn uint64
		err := rows.Scan(&bn)
		if err != nil {
			if err == sql.ErrNoRows {
				http.Error(w, "Row not found", http.StatusNotFound)
			} else {
				http.Error(w, "Internal server error", http.StatusInternalServerError)
			}
			log.Printf("An error occurred during scan sql response: %s", err)
			return
		}
		blockNumbers = append(blockNumbers, bn)
	}

	blockLatest = BlockLatestResponse{
		EthereumBlockLatest:                   blockNumbers[0],
		PolygonBlockLatest:                    blockNumbers[1],
		PolygonBlockLatestLabelsMoonwormAlpha: blockNumbers[2],
	}

	json.NewEncoder(w).Encode(blockLatest)
}
