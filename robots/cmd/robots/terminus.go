package main

import (
	"math/big"

	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/ethclient"

	terminus_contract "github.com/bugout-dev/engine/robots/pkg/terminus"
)

type ContractTerminusInstance struct {
	Address        common.Address
	Instance       *terminus_contract.Terminus
	TerminusPoolId int64
}

func GetTerminusContractAddress(terminusAddress string) common.Address {
	return common.HexToAddress(terminusAddress)
}

// InitializeContractInstance parse contract to instance
func InitializeTerminusContractInstance(client *ethclient.Client, address common.Address) (*terminus_contract.Terminus, error) {
	contractInstance, err := terminus_contract.NewTerminus(address, client)
	if err != nil {
		return nil, err
	}

	return contractInstance, nil
}

func (ct *ContractTerminusInstance) FetchPoolCapacity(pool_id int64) (*big.Int, error) {
	pool_capacity, err := ct.Instance.TerminusPoolCapacity(nil, big.NewInt(pool_id))
	if err != nil {
		return nil, err
	}

	return pool_capacity, nil
}

// PoolMintBatch executes PoolMintBatch for list of address with same value amount
func (cti *ContractTerminusInstance) PoolMintBatch(auth *bind.TransactOpts, claimants []Claimant, value int64) (*types.Transaction, error) {
	to_addresses := []common.Address{}
	values := []*big.Int{}
	for _, claimant := range claimants {
		to_addresses = append(to_addresses, common.HexToAddress(claimant.Address))
		values = append(values, big.NewInt(value))
	}

	tx, err := cti.Instance.PoolMintBatch(auth, big.NewInt(cti.TerminusPoolId), to_addresses, values)
	if err != nil {
		return nil, err
	}

	return tx, nil
}

func (cti *ContractTerminusInstance) BalanceOfBatch(auth *bind.CallOpts, claimants []Claimant, id_int int64) ([]*big.Int, error) {
	addresses := []common.Address{}
	ids := []*big.Int{}
	for _, claimant := range claimants {
		addresses = append(addresses, common.HexToAddress(claimant.Address))
		ids = append(ids, big.NewInt(id_int))
	}
	balances, err := cti.Instance.BalanceOfBatch(auth, addresses, ids)
	if err != nil {
		return nil, err
	}

	return balances, nil
}
