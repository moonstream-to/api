package main

import (
	"context"
	"errors"
	"fmt"
	"math/big"

	"github.com/ethereum/go-ethereum/ethclient"
)

type NetworkClient struct {
	Endpoint string
	ChainID  *big.Int
}

type NetworkInstance struct {
	Blockchain string
	Endpoint   string
	ChainID    *big.Int

	Client *ethclient.Client

	GasPrice *big.Int
}

func InitializeNetworks() (map[string]NetworkClient, error) {
	networks := make(map[string]NetworkClient)

	if NODEBALANCER_ACCESS_ID == "" {
		return nil, errors.New("Environment variable ENGINE_NODEBALANCER_ACCESS_ID should be specified")
	}

	if MUMBAI_WEB3_PROVIDER_URI == "" {
		return nil, errors.New("Environment variable MUMBAI_WEB3_PROVIDER_URI should be specified")
	}
	if POLYGON_WEB3_PROVIDER_URI == "" {
		return nil, errors.New("Environment variable POLYGON_WEB3_PROVIDER_URI should be specified")
	}
	if WYRM_WEB3_PROVIDER_URI == "" {
		return nil, errors.New("Environment variable MOONSTREAM_WYRM_WEB3_PROVIDER_URI should be specified")
	}

	networks["mumbai"] = NetworkClient{
		Endpoint: fmt.Sprintf("%s?access_id=%s&data_source=blockchain", MUMBAI_WEB3_PROVIDER_URI, NODEBALANCER_ACCESS_ID),
		ChainID:  big.NewInt(80001),
	}
	networks["polygon"] = NetworkClient{
		Endpoint: fmt.Sprintf("%s?access_id=%s&data_source=blockchain", POLYGON_WEB3_PROVIDER_URI, NODEBALANCER_ACCESS_ID),
		ChainID:  big.NewInt(137),
	}
	networks["wyrm"] = NetworkClient{
		Endpoint: WYRM_WEB3_PROVIDER_URI,
		ChainID:  big.NewInt(322),
	}

	return networks, nil
}

// GenDialRpcClient parse PRC endpoint to dial client
func GenDialRpcClient(rpc_endpoint_uri string) (*ethclient.Client, error) {
	client, err := ethclient.Dial(rpc_endpoint_uri)
	if err != nil {
		return nil, err
	}

	return client, nil
}

// FetchSuggestedGasPrice fetch network for suggested gas price
func (ni *NetworkInstance) FetchSuggestedGasPrice(ctx context.Context) error {
	gas_price, err := ni.Client.SuggestGasPrice(ctx)
	if err != nil {
		return err
	}

	ni.GasPrice = gas_price

	return nil
}
