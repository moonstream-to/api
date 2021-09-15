package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type PingResponse struct {
	Status string `json:"status"`
}

func ping(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

func main() {
	address := "0.0.0.0:8931"
	fmt.Printf("Starting server at %s\n", address)

	http.HandleFunc("/ping", ping)

	http.ListenAndServe(address, nil)
}
