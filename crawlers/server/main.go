package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
)

var MOONSTREAM_IPC_PATH = os.Getenv("MOONSTREAM_IPC_PATH")
var MOONSTREAM_CORS_ALLOWED_ORIGINS = os.Getenv("MOONSTREAM_CORS_ALLOWED_ORIGINS")

type GethResponse struct {
	Result string `json:"result"`
}

type PingGethResponse struct {
	CurrentBlock uint64 `json:"current_block"`
}

type PingResponse struct {
	Status string `json:"status"`
}

// Extends handler with allowed CORS policies
func setupCorsResponse(w *http.ResponseWriter, req *http.Request) {
	for _, allowedOrigin := range strings.Split(MOONSTREAM_CORS_ALLOWED_ORIGINS, ",") {
		for _, reqOrigin := range req.Header["Origin"] {
			if reqOrigin == allowedOrigin {
				(*w).Header().Set("Access-Control-Allow-Origin", allowedOrigin)
			}
		}

	}
	(*w).Header().Set("Access-Control-Allow-Methods", "GET,OPTIONS")
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

func pingGeth(w http.ResponseWriter, req *http.Request) {
	setupCorsResponse(&w, req)
	log.Printf("%s, %s, %q", req.RemoteAddr, req.Method, req.URL.String())
	if (*req).Method == "OPTIONS" {
		return
	}

	postBody, err := json.Marshal(map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  "eth_blockNumber",
		"params":  []string{},
		"id":      1,
	})
	if err != nil {
		log.Println(err)
		http.Error(w, http.StatusText(500), 500)
		return
	}
	gethResponse, err := http.Post(MOONSTREAM_IPC_PATH, "application/json",
		bytes.NewBuffer(postBody))
	if err != nil {
		log.Printf("Unable to request geth, error: %v", err)
		http.Error(w, http.StatusText(500), 500)
		return
	}
	defer gethResponse.Body.Close()

	gethResponseBody, err := ioutil.ReadAll(gethResponse.Body)
	if err != nil {
		log.Printf("Unable to read geth response, error: %v", err)
		http.Error(w, http.StatusText(500), 500)
		return
	}
	var obj GethResponse
	_ = json.Unmarshal(gethResponseBody, &obj)

	blockNumberHex := strings.Replace(obj.Result, "0x", "", -1)
	blockNumberStr, err := strconv.ParseUint(blockNumberHex, 16, 64)
	if err != nil {
		log.Printf("Unable to parse block number from hex to string, error: %v", err)
		http.Error(w, http.StatusText(500), 500)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	response := PingGethResponse{CurrentBlock: blockNumberStr}
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
	http.HandleFunc("/status", pingGeth)

	http.ListenAndServe(address, nil)
}
