package mooncrawl

import (
	"context"
	"encoding/json"
	"fmt"
	"math/big"
	"sync"
	// "sync/atomic"

	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/ethereum/go-ethereum/rpc"
	"github.com/ethereum/go-ethereum/internal/ethapi"
	// "github.com/ethereum/go-ethereum/rpc/comms"
)

type ClientHandler struct {
	*ethclient.Client
}

type API struct {
	client rpc.Client // RPC client with a live connection to an Ethereum node
	autoid uint32     // ID number to use for the next API request
	lock   sync.Mutex // Singleton access until we get to request multiplexing
}

// request is a JSON RPC request package assembled internally from the client
// method calls.
type request struct {
	JsonRpc string        `json:"jsonrpc"` // Version of the JSON RPC protocol, always set to 2.0
	Id      int           `json:"id"`      // Auto incrementing ID number for this request
	Method  string        `json:"method"`  // Remote procedure name to invoke on the server
	Params  []interface{} `json:"params"`  // List of parameters to pass through (keep types simple)
}

// response is a JSON RPC response package sent back from the API server.
type response struct {
	JsonRpc string          `json:"jsonrpc"` // Version of the JSON RPC protocol, always set to 2.0
	Id      int             `json:"id"`      // Auto incrementing ID number for this request
	Error   json.RawMessage `json:"error"`   // Any error returned by the remote side
	Result  json.RawMessage `json:"result"`  // Whatever the remote side sends us in reply
}

// func (api *API) Request(method string, params []interface{}) (json.RawMessage, error) {
// 	api.lock.Lock()
// 	defer api.lock.Unlock()

// 	// Ugly hack to serialize an empty list properly
// 	if params == nil {
// 		params = []interface{}{}
// 	}
// 	// Assemble the request object
// 	req := &request{
// 		JsonRpc: "2.0",
// 		Id:      int(atomic.AddUint32(&api.autoid, 1)),
// 		Method:  method,
// 		Params:  params,
// 	}
// 	if err := api.client.Vall(req); err != nil {
// 		return nil, err
// 	}
// 	res := new(response)
// 	if err := api.client.Recv(res); err != nil {
// 		return nil, err
// 	}
// 	if len(res.Error) > 0 {
// 		return nil, fmt.Errorf("remote error: %s", string(res.Error))
// 	}
// 	return res.Result, nil
// }

func PrBlock(client *ethclient.Client) {
	// ctx, _ := context.WithDeadline(context.Background(), time.Now().Add(2 * time.Second))
	block, err := client.BlockByNumber(context.Background(), big.NewInt(12000001))
	// block, _ := client.BlockNumber(context.Background())
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(block)
}

func Client() {
	// const ethClientUri string = "http://127.0.0.1:18375"
	// client, err := ethclient.Dial(ethClientUri)
	// return client, err
	
	// '{"id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}'
	// req := &request{
	// 	JsonRpc: "2.0",
	// 	Id:      int(atomic.AddUint32(&api.autoid, 1)),
	// 	Method:  "eth_subscribe",
	// 	Params:  ["newPendingTransactions"],
	// }

	wsConn, err := rpc.DialWebsocket(context.Background(), "ws://127.0.0.1:18376", "")
	if err != nil {
		panic(err)
	}
	defer wsConn.Close()

	// type params []interface{}

	// client := ethclient.NewClient(wsConn)
	// block, _ := client.BlockByNumber(context.Background(), big.NewInt(12000001))
	// fmt.Println(block)

	// client.TransactionReceipt(context.Background(), tx.Hash())
	// wsConn.CallContext

	ch := make(chan interface{})
	defer close(ch)

	sub, err := wsConn.Subscribe(context.Background(), "txpool_content", ch)
	if err != nil {
		panic(err)
	}
	fmt.Println(sub)
	defer sub.Unsubscribe()
}
