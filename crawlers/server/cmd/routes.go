package cmd

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"

	settings "github.com/bugout-dev/moonstream/crawlers/server/configs"
)

func pingRoute(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := PingResponse{Status: "ok"}
	json.NewEncoder(w).Encode(response)
}

// Fetch latest block from Geth
func pingGethRoute(w http.ResponseWriter, req *http.Request) {
	postBody, err := json.Marshal(map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  "eth_blockNumber",
		"params":  []string{},
		"id":      1,
	})
	if err != nil {
		log.Printf("An error occurred due marshal postBody, error: %s", err)
		http.Error(w, http.StatusText(500), http.StatusInternalServerError)
		return
	}
	gethResponse, err := http.Post(settings.MOONSTREAM_IPC_PATH, "application/json",
		bytes.NewBuffer(postBody))
	if err != nil {
		log.Printf("Unable to request geth, error: %s", err)
		http.Error(w, http.StatusText(500), http.StatusInternalServerError)
		return
	}
	defer gethResponse.Body.Close()

	gethResponseBody, err := ioutil.ReadAll(gethResponse.Body)
	if err != nil {
		log.Printf("Unable to read geth response, error: %s", err)
		http.Error(w, http.StatusText(500), http.StatusInternalServerError)
		return
	}
	var obj GethResponse
	_ = json.Unmarshal(gethResponseBody, &obj)

	blockNumberHex := strings.Replace(obj.Result, "0x", "", -1)
	blockNumberStr, err := strconv.ParseUint(blockNumberHex, 16, 64)
	if err != nil {
		log.Printf("Unable to parse block number from hex to string, error: %s", err)
		http.Error(w, http.StatusText(500), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	response := PingGethResponse{CurrentBlock: blockNumberStr}
	json.NewEncoder(w).Encode(response)
}
