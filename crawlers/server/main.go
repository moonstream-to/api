package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

var MOONSTREAM_IPC_PATH = os.Getenv("MOONSTREAM_DB_URI")

type GethEthSyncingResponse struct {
	CurrentBlock string `json:"currentBlock"`
}

type GethResponse struct {
	Result GethEthSyncingResponse `json:"result"`
}

type PingGethResponse struct {
	Status       string `json:"status"`
	CurrentBlock string `json:"current_block"`
}

type PingResponse struct {
	Status string `json:"status"`
}

func ping(w http.ResponseWriter, req *http.Request) {
	log.Printf("%s, %s, %q", req.RemoteAddr, req.Method, req.URL.String())

	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

func pingGeth(w http.ResponseWriter, req *http.Request) {
	log.Printf("%s, %s, %q", req.RemoteAddr, req.Method, req.URL.String())

	postBody, err := json.Marshal(map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  "eth_syncing",
		"id":      1,
	})
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}
	gethResponse, err := http.Post(MOONSTREAM_IPC_PATH, "application/json",
		bytes.NewBuffer(postBody))
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}
	defer gethResponse.Body.Close()

	gethResponseBody, err := ioutil.ReadAll(gethResponse.Body)
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}
	var obj GethResponse
	_ = json.Unmarshal(gethResponseBody, &obj)

	w.Header().Set("Content-Type", "application/json")
	response := PingGethResponse{Status: "ok", CurrentBlock: obj.Result.CurrentBlock}
	json.NewEncoder(w).Encode(response)
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
	http.HandleFunc("/ping/geth", pingGeth)

	http.ListenAndServe(address, nil)
}
