// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package terminus

import (
	"errors"
	"math/big"
	"strings"

	ethereum "github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/event"
)

// Reference imports to suppress errors if they are not otherwise used.
var (
	_ = errors.New
	_ = big.NewInt
	_ = strings.NewReader
	_ = ethereum.NotFound
	_ = bind.Bind
	_ = common.Big1
	_ = types.BloomLookup
	_ = event.NewSubscription
)

// TerminusMetaData contains all meta data concerning the Terminus contract.
var TerminusMetaData = &bind.MetaData{
	ABI: "[{\"inputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"bool\",\"name\":\"approved\",\"type\":\"bool\"}],\"name\":\"ApprovalForAll\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"uint256\",\"name\":\"id\",\"type\":\"uint256\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"address\",\"name\":\"from\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"address[]\",\"name\":\"toAddresses\",\"type\":\"address[]\"},{\"indexed\":false,\"internalType\":\"uint256[]\",\"name\":\"amounts\",\"type\":\"uint256[]\"}],\"name\":\"PoolMintBatch\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"from\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"to\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256[]\",\"name\":\"ids\",\"type\":\"uint256[]\"},{\"indexed\":false,\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"}],\"name\":\"TransferBatch\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"from\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"to\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"id\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"TransferSingle\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"string\",\"name\":\"value\",\"type\":\"string\"},{\"indexed\":true,\"internalType\":\"uint256\",\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"URI\",\"type\":\"event\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"}],\"name\":\"approveForPool\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"id\",\"type\":\"uint256\"}],\"name\":\"balanceOf\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"accounts\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"ids\",\"type\":\"uint256[]\"}],\"name\":\"balanceOfBatch\",\"outputs\":[{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"from\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"burn\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"contractURI\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"_capacity\",\"type\":\"uint256\"},{\"internalType\":\"bool\",\"name\":\"_transferable\",\"type\":\"bool\"},{\"internalType\":\"bool\",\"name\":\"_burnable\",\"type\":\"bool\"}],\"name\":\"createPoolV1\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"_capacity\",\"type\":\"uint256\"}],\"name\":\"createSimplePool\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"}],\"name\":\"isApprovedForAll\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"}],\"name\":\"isApprovedForPool\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"to\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"},{\"internalType\":\"bytes\",\"name\":\"data\",\"type\":\"bytes\"}],\"name\":\"mint\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"to\",\"type\":\"address\"},{\"internalType\":\"uint256[]\",\"name\":\"poolIDs\",\"type\":\"uint256[]\"},{\"internalType\":\"uint256[]\",\"name\":\"amounts\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes\",\"name\":\"data\",\"type\":\"bytes\"}],\"name\":\"mintBatch\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"paymentToken\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"poolBasePrice\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"id\",\"type\":\"uint256\"},{\"internalType\":\"address[]\",\"name\":\"toAddresses\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"amounts\",\"type\":\"uint256[]\"}],\"name\":\"poolMintBatch\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"from\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"to\",\"type\":\"address\"},{\"internalType\":\"uint256[]\",\"name\":\"ids\",\"type\":\"uint256[]\"},{\"internalType\":\"uint256[]\",\"name\":\"amounts\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes\",\"name\":\"data\",\"type\":\"bytes\"}],\"name\":\"safeBatchTransferFrom\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"from\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"to\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"id\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"},{\"internalType\":\"bytes\",\"name\":\"data\",\"type\":\"bytes\"}],\"name\":\"safeTransferFrom\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"operator\",\"type\":\"address\"},{\"internalType\":\"bool\",\"name\":\"approved\",\"type\":\"bool\"}],\"name\":\"setApprovalForAll\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"string\",\"name\":\"_contractURI\",\"type\":\"string\"}],\"name\":\"setContractURI\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"newPaymentToken\",\"type\":\"address\"}],\"name\":\"setPaymentToken\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"newBasePrice\",\"type\":\"uint256\"}],\"name\":\"setPoolBasePrice\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"newController\",\"type\":\"address\"}],\"name\":\"setPoolController\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"},{\"internalType\":\"string\",\"name\":\"poolURI\",\"type\":\"string\"}],\"name\":\"setURI\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"bytes4\",\"name\":\"interfaceId\",\"type\":\"bytes4\"}],\"name\":\"supportsInterface\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"terminusController\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"}],\"name\":\"terminusPoolCapacity\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"}],\"name\":\"terminusPoolController\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"}],\"name\":\"terminusPoolSupply\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"totalPools\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"poolID\",\"type\":\"uint256\"}],\"name\":\"uri\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"toAddress\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"withdrawPayments\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
}

// TerminusABI is the input ABI used to generate the binding from.
// Deprecated: Use TerminusMetaData.ABI instead.
var TerminusABI = TerminusMetaData.ABI

// Terminus is an auto generated Go binding around an Ethereum contract.
type Terminus struct {
	TerminusCaller     // Read-only binding to the contract
	TerminusTransactor // Write-only binding to the contract
	TerminusFilterer   // Log filterer for contract events
}

// TerminusCaller is an auto generated read-only Go binding around an Ethereum contract.
type TerminusCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// TerminusTransactor is an auto generated write-only Go binding around an Ethereum contract.
type TerminusTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// TerminusFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type TerminusFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// TerminusSession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type TerminusSession struct {
	Contract     *Terminus         // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// TerminusCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type TerminusCallerSession struct {
	Contract *TerminusCaller // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts   // Call options to use throughout this session
}

// TerminusTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type TerminusTransactorSession struct {
	Contract     *TerminusTransactor // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts   // Transaction auth options to use throughout this session
}

// TerminusRaw is an auto generated low-level Go binding around an Ethereum contract.
type TerminusRaw struct {
	Contract *Terminus // Generic contract binding to access the raw methods on
}

// TerminusCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type TerminusCallerRaw struct {
	Contract *TerminusCaller // Generic read-only contract binding to access the raw methods on
}

// TerminusTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type TerminusTransactorRaw struct {
	Contract *TerminusTransactor // Generic write-only contract binding to access the raw methods on
}

// NewTerminus creates a new instance of Terminus, bound to a specific deployed contract.
func NewTerminus(address common.Address, backend bind.ContractBackend) (*Terminus, error) {
	contract, err := bindTerminus(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &Terminus{TerminusCaller: TerminusCaller{contract: contract}, TerminusTransactor: TerminusTransactor{contract: contract}, TerminusFilterer: TerminusFilterer{contract: contract}}, nil
}

// NewTerminusCaller creates a new read-only instance of Terminus, bound to a specific deployed contract.
func NewTerminusCaller(address common.Address, caller bind.ContractCaller) (*TerminusCaller, error) {
	contract, err := bindTerminus(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &TerminusCaller{contract: contract}, nil
}

// NewTerminusTransactor creates a new write-only instance of Terminus, bound to a specific deployed contract.
func NewTerminusTransactor(address common.Address, transactor bind.ContractTransactor) (*TerminusTransactor, error) {
	contract, err := bindTerminus(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &TerminusTransactor{contract: contract}, nil
}

// NewTerminusFilterer creates a new log filterer instance of Terminus, bound to a specific deployed contract.
func NewTerminusFilterer(address common.Address, filterer bind.ContractFilterer) (*TerminusFilterer, error) {
	contract, err := bindTerminus(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &TerminusFilterer{contract: contract}, nil
}

// bindTerminus binds a generic wrapper to an already deployed contract.
func bindTerminus(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := abi.JSON(strings.NewReader(TerminusABI))
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Terminus *TerminusRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Terminus.Contract.TerminusCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Terminus *TerminusRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Terminus.Contract.TerminusTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Terminus *TerminusRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Terminus.Contract.TerminusTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Terminus *TerminusCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Terminus.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Terminus *TerminusTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Terminus.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Terminus *TerminusTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Terminus.Contract.contract.Transact(opts, method, params...)
}

// BalanceOf is a free data retrieval call binding the contract method 0x00fdd58e.
//
// Solidity: function balanceOf(address account, uint256 id) view returns(uint256)
func (_Terminus *TerminusCaller) BalanceOf(opts *bind.CallOpts, account common.Address, id *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "balanceOf", account, id)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// BalanceOf is a free data retrieval call binding the contract method 0x00fdd58e.
//
// Solidity: function balanceOf(address account, uint256 id) view returns(uint256)
func (_Terminus *TerminusSession) BalanceOf(account common.Address, id *big.Int) (*big.Int, error) {
	return _Terminus.Contract.BalanceOf(&_Terminus.CallOpts, account, id)
}

// BalanceOf is a free data retrieval call binding the contract method 0x00fdd58e.
//
// Solidity: function balanceOf(address account, uint256 id) view returns(uint256)
func (_Terminus *TerminusCallerSession) BalanceOf(account common.Address, id *big.Int) (*big.Int, error) {
	return _Terminus.Contract.BalanceOf(&_Terminus.CallOpts, account, id)
}

// BalanceOfBatch is a free data retrieval call binding the contract method 0x4e1273f4.
//
// Solidity: function balanceOfBatch(address[] accounts, uint256[] ids) view returns(uint256[])
func (_Terminus *TerminusCaller) BalanceOfBatch(opts *bind.CallOpts, accounts []common.Address, ids []*big.Int) ([]*big.Int, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "balanceOfBatch", accounts, ids)

	if err != nil {
		return *new([]*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new([]*big.Int)).(*[]*big.Int)

	return out0, err

}

// BalanceOfBatch is a free data retrieval call binding the contract method 0x4e1273f4.
//
// Solidity: function balanceOfBatch(address[] accounts, uint256[] ids) view returns(uint256[])
func (_Terminus *TerminusSession) BalanceOfBatch(accounts []common.Address, ids []*big.Int) ([]*big.Int, error) {
	return _Terminus.Contract.BalanceOfBatch(&_Terminus.CallOpts, accounts, ids)
}

// BalanceOfBatch is a free data retrieval call binding the contract method 0x4e1273f4.
//
// Solidity: function balanceOfBatch(address[] accounts, uint256[] ids) view returns(uint256[])
func (_Terminus *TerminusCallerSession) BalanceOfBatch(accounts []common.Address, ids []*big.Int) ([]*big.Int, error) {
	return _Terminus.Contract.BalanceOfBatch(&_Terminus.CallOpts, accounts, ids)
}

// ContractURI is a free data retrieval call binding the contract method 0xe8a3d485.
//
// Solidity: function contractURI() view returns(string)
func (_Terminus *TerminusCaller) ContractURI(opts *bind.CallOpts) (string, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "contractURI")

	if err != nil {
		return *new(string), err
	}

	out0 := *abi.ConvertType(out[0], new(string)).(*string)

	return out0, err

}

// ContractURI is a free data retrieval call binding the contract method 0xe8a3d485.
//
// Solidity: function contractURI() view returns(string)
func (_Terminus *TerminusSession) ContractURI() (string, error) {
	return _Terminus.Contract.ContractURI(&_Terminus.CallOpts)
}

// ContractURI is a free data retrieval call binding the contract method 0xe8a3d485.
//
// Solidity: function contractURI() view returns(string)
func (_Terminus *TerminusCallerSession) ContractURI() (string, error) {
	return _Terminus.Contract.ContractURI(&_Terminus.CallOpts)
}

// IsApprovedForAll is a free data retrieval call binding the contract method 0xe985e9c5.
//
// Solidity: function isApprovedForAll(address account, address operator) view returns(bool)
func (_Terminus *TerminusCaller) IsApprovedForAll(opts *bind.CallOpts, account common.Address, operator common.Address) (bool, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "isApprovedForAll", account, operator)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// IsApprovedForAll is a free data retrieval call binding the contract method 0xe985e9c5.
//
// Solidity: function isApprovedForAll(address account, address operator) view returns(bool)
func (_Terminus *TerminusSession) IsApprovedForAll(account common.Address, operator common.Address) (bool, error) {
	return _Terminus.Contract.IsApprovedForAll(&_Terminus.CallOpts, account, operator)
}

// IsApprovedForAll is a free data retrieval call binding the contract method 0xe985e9c5.
//
// Solidity: function isApprovedForAll(address account, address operator) view returns(bool)
func (_Terminus *TerminusCallerSession) IsApprovedForAll(account common.Address, operator common.Address) (bool, error) {
	return _Terminus.Contract.IsApprovedForAll(&_Terminus.CallOpts, account, operator)
}

// IsApprovedForPool is a free data retrieval call binding the contract method 0x027b3fc2.
//
// Solidity: function isApprovedForPool(uint256 poolID, address operator) view returns(bool)
func (_Terminus *TerminusCaller) IsApprovedForPool(opts *bind.CallOpts, poolID *big.Int, operator common.Address) (bool, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "isApprovedForPool", poolID, operator)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// IsApprovedForPool is a free data retrieval call binding the contract method 0x027b3fc2.
//
// Solidity: function isApprovedForPool(uint256 poolID, address operator) view returns(bool)
func (_Terminus *TerminusSession) IsApprovedForPool(poolID *big.Int, operator common.Address) (bool, error) {
	return _Terminus.Contract.IsApprovedForPool(&_Terminus.CallOpts, poolID, operator)
}

// IsApprovedForPool is a free data retrieval call binding the contract method 0x027b3fc2.
//
// Solidity: function isApprovedForPool(uint256 poolID, address operator) view returns(bool)
func (_Terminus *TerminusCallerSession) IsApprovedForPool(poolID *big.Int, operator common.Address) (bool, error) {
	return _Terminus.Contract.IsApprovedForPool(&_Terminus.CallOpts, poolID, operator)
}

// PaymentToken is a free data retrieval call binding the contract method 0x3013ce29.
//
// Solidity: function paymentToken() view returns(address)
func (_Terminus *TerminusCaller) PaymentToken(opts *bind.CallOpts) (common.Address, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "paymentToken")

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// PaymentToken is a free data retrieval call binding the contract method 0x3013ce29.
//
// Solidity: function paymentToken() view returns(address)
func (_Terminus *TerminusSession) PaymentToken() (common.Address, error) {
	return _Terminus.Contract.PaymentToken(&_Terminus.CallOpts)
}

// PaymentToken is a free data retrieval call binding the contract method 0x3013ce29.
//
// Solidity: function paymentToken() view returns(address)
func (_Terminus *TerminusCallerSession) PaymentToken() (common.Address, error) {
	return _Terminus.Contract.PaymentToken(&_Terminus.CallOpts)
}

// PoolBasePrice is a free data retrieval call binding the contract method 0x8925d013.
//
// Solidity: function poolBasePrice() view returns(uint256)
func (_Terminus *TerminusCaller) PoolBasePrice(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "poolBasePrice")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// PoolBasePrice is a free data retrieval call binding the contract method 0x8925d013.
//
// Solidity: function poolBasePrice() view returns(uint256)
func (_Terminus *TerminusSession) PoolBasePrice() (*big.Int, error) {
	return _Terminus.Contract.PoolBasePrice(&_Terminus.CallOpts)
}

// PoolBasePrice is a free data retrieval call binding the contract method 0x8925d013.
//
// Solidity: function poolBasePrice() view returns(uint256)
func (_Terminus *TerminusCallerSession) PoolBasePrice() (*big.Int, error) {
	return _Terminus.Contract.PoolBasePrice(&_Terminus.CallOpts)
}

// SupportsInterface is a free data retrieval call binding the contract method 0x01ffc9a7.
//
// Solidity: function supportsInterface(bytes4 interfaceId) view returns(bool)
func (_Terminus *TerminusCaller) SupportsInterface(opts *bind.CallOpts, interfaceId [4]byte) (bool, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "supportsInterface", interfaceId)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// SupportsInterface is a free data retrieval call binding the contract method 0x01ffc9a7.
//
// Solidity: function supportsInterface(bytes4 interfaceId) view returns(bool)
func (_Terminus *TerminusSession) SupportsInterface(interfaceId [4]byte) (bool, error) {
	return _Terminus.Contract.SupportsInterface(&_Terminus.CallOpts, interfaceId)
}

// SupportsInterface is a free data retrieval call binding the contract method 0x01ffc9a7.
//
// Solidity: function supportsInterface(bytes4 interfaceId) view returns(bool)
func (_Terminus *TerminusCallerSession) SupportsInterface(interfaceId [4]byte) (bool, error) {
	return _Terminus.Contract.SupportsInterface(&_Terminus.CallOpts, interfaceId)
}

// TerminusController is a free data retrieval call binding the contract method 0x366e59e3.
//
// Solidity: function terminusController() view returns(address)
func (_Terminus *TerminusCaller) TerminusController(opts *bind.CallOpts) (common.Address, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "terminusController")

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// TerminusController is a free data retrieval call binding the contract method 0x366e59e3.
//
// Solidity: function terminusController() view returns(address)
func (_Terminus *TerminusSession) TerminusController() (common.Address, error) {
	return _Terminus.Contract.TerminusController(&_Terminus.CallOpts)
}

// TerminusController is a free data retrieval call binding the contract method 0x366e59e3.
//
// Solidity: function terminusController() view returns(address)
func (_Terminus *TerminusCallerSession) TerminusController() (common.Address, error) {
	return _Terminus.Contract.TerminusController(&_Terminus.CallOpts)
}

// TerminusPoolCapacity is a free data retrieval call binding the contract method 0x5dc8bdf8.
//
// Solidity: function terminusPoolCapacity(uint256 poolID) view returns(uint256)
func (_Terminus *TerminusCaller) TerminusPoolCapacity(opts *bind.CallOpts, poolID *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "terminusPoolCapacity", poolID)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// TerminusPoolCapacity is a free data retrieval call binding the contract method 0x5dc8bdf8.
//
// Solidity: function terminusPoolCapacity(uint256 poolID) view returns(uint256)
func (_Terminus *TerminusSession) TerminusPoolCapacity(poolID *big.Int) (*big.Int, error) {
	return _Terminus.Contract.TerminusPoolCapacity(&_Terminus.CallOpts, poolID)
}

// TerminusPoolCapacity is a free data retrieval call binding the contract method 0x5dc8bdf8.
//
// Solidity: function terminusPoolCapacity(uint256 poolID) view returns(uint256)
func (_Terminus *TerminusCallerSession) TerminusPoolCapacity(poolID *big.Int) (*big.Int, error) {
	return _Terminus.Contract.TerminusPoolCapacity(&_Terminus.CallOpts, poolID)
}

// TerminusPoolController is a free data retrieval call binding the contract method 0xd0c402e5.
//
// Solidity: function terminusPoolController(uint256 poolID) view returns(address)
func (_Terminus *TerminusCaller) TerminusPoolController(opts *bind.CallOpts, poolID *big.Int) (common.Address, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "terminusPoolController", poolID)

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// TerminusPoolController is a free data retrieval call binding the contract method 0xd0c402e5.
//
// Solidity: function terminusPoolController(uint256 poolID) view returns(address)
func (_Terminus *TerminusSession) TerminusPoolController(poolID *big.Int) (common.Address, error) {
	return _Terminus.Contract.TerminusPoolController(&_Terminus.CallOpts, poolID)
}

// TerminusPoolController is a free data retrieval call binding the contract method 0xd0c402e5.
//
// Solidity: function terminusPoolController(uint256 poolID) view returns(address)
func (_Terminus *TerminusCallerSession) TerminusPoolController(poolID *big.Int) (common.Address, error) {
	return _Terminus.Contract.TerminusPoolController(&_Terminus.CallOpts, poolID)
}

// TerminusPoolSupply is a free data retrieval call binding the contract method 0xa44cfc82.
//
// Solidity: function terminusPoolSupply(uint256 poolID) view returns(uint256)
func (_Terminus *TerminusCaller) TerminusPoolSupply(opts *bind.CallOpts, poolID *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "terminusPoolSupply", poolID)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// TerminusPoolSupply is a free data retrieval call binding the contract method 0xa44cfc82.
//
// Solidity: function terminusPoolSupply(uint256 poolID) view returns(uint256)
func (_Terminus *TerminusSession) TerminusPoolSupply(poolID *big.Int) (*big.Int, error) {
	return _Terminus.Contract.TerminusPoolSupply(&_Terminus.CallOpts, poolID)
}

// TerminusPoolSupply is a free data retrieval call binding the contract method 0xa44cfc82.
//
// Solidity: function terminusPoolSupply(uint256 poolID) view returns(uint256)
func (_Terminus *TerminusCallerSession) TerminusPoolSupply(poolID *big.Int) (*big.Int, error) {
	return _Terminus.Contract.TerminusPoolSupply(&_Terminus.CallOpts, poolID)
}

// TotalPools is a free data retrieval call binding the contract method 0xab3c7e52.
//
// Solidity: function totalPools() view returns(uint256)
func (_Terminus *TerminusCaller) TotalPools(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "totalPools")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// TotalPools is a free data retrieval call binding the contract method 0xab3c7e52.
//
// Solidity: function totalPools() view returns(uint256)
func (_Terminus *TerminusSession) TotalPools() (*big.Int, error) {
	return _Terminus.Contract.TotalPools(&_Terminus.CallOpts)
}

// TotalPools is a free data retrieval call binding the contract method 0xab3c7e52.
//
// Solidity: function totalPools() view returns(uint256)
func (_Terminus *TerminusCallerSession) TotalPools() (*big.Int, error) {
	return _Terminus.Contract.TotalPools(&_Terminus.CallOpts)
}

// Uri is a free data retrieval call binding the contract method 0x0e89341c.
//
// Solidity: function uri(uint256 poolID) view returns(string)
func (_Terminus *TerminusCaller) Uri(opts *bind.CallOpts, poolID *big.Int) (string, error) {
	var out []interface{}
	err := _Terminus.contract.Call(opts, &out, "uri", poolID)

	if err != nil {
		return *new(string), err
	}

	out0 := *abi.ConvertType(out[0], new(string)).(*string)

	return out0, err

}

// Uri is a free data retrieval call binding the contract method 0x0e89341c.
//
// Solidity: function uri(uint256 poolID) view returns(string)
func (_Terminus *TerminusSession) Uri(poolID *big.Int) (string, error) {
	return _Terminus.Contract.Uri(&_Terminus.CallOpts, poolID)
}

// Uri is a free data retrieval call binding the contract method 0x0e89341c.
//
// Solidity: function uri(uint256 poolID) view returns(string)
func (_Terminus *TerminusCallerSession) Uri(poolID *big.Int) (string, error) {
	return _Terminus.Contract.Uri(&_Terminus.CallOpts, poolID)
}

// ApproveForPool is a paid mutator transaction binding the contract method 0x85bc82e2.
//
// Solidity: function approveForPool(uint256 poolID, address operator) returns()
func (_Terminus *TerminusTransactor) ApproveForPool(opts *bind.TransactOpts, poolID *big.Int, operator common.Address) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "approveForPool", poolID, operator)
}

// ApproveForPool is a paid mutator transaction binding the contract method 0x85bc82e2.
//
// Solidity: function approveForPool(uint256 poolID, address operator) returns()
func (_Terminus *TerminusSession) ApproveForPool(poolID *big.Int, operator common.Address) (*types.Transaction, error) {
	return _Terminus.Contract.ApproveForPool(&_Terminus.TransactOpts, poolID, operator)
}

// ApproveForPool is a paid mutator transaction binding the contract method 0x85bc82e2.
//
// Solidity: function approveForPool(uint256 poolID, address operator) returns()
func (_Terminus *TerminusTransactorSession) ApproveForPool(poolID *big.Int, operator common.Address) (*types.Transaction, error) {
	return _Terminus.Contract.ApproveForPool(&_Terminus.TransactOpts, poolID, operator)
}

// Burn is a paid mutator transaction binding the contract method 0xf5298aca.
//
// Solidity: function burn(address from, uint256 poolID, uint256 amount) returns()
func (_Terminus *TerminusTransactor) Burn(opts *bind.TransactOpts, from common.Address, poolID *big.Int, amount *big.Int) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "burn", from, poolID, amount)
}

// Burn is a paid mutator transaction binding the contract method 0xf5298aca.
//
// Solidity: function burn(address from, uint256 poolID, uint256 amount) returns()
func (_Terminus *TerminusSession) Burn(from common.Address, poolID *big.Int, amount *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.Burn(&_Terminus.TransactOpts, from, poolID, amount)
}

// Burn is a paid mutator transaction binding the contract method 0xf5298aca.
//
// Solidity: function burn(address from, uint256 poolID, uint256 amount) returns()
func (_Terminus *TerminusTransactorSession) Burn(from common.Address, poolID *big.Int, amount *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.Burn(&_Terminus.TransactOpts, from, poolID, amount)
}

// CreatePoolV1 is a paid mutator transaction binding the contract method 0x3bad2d82.
//
// Solidity: function createPoolV1(uint256 _capacity, bool _transferable, bool _burnable) returns(uint256)
func (_Terminus *TerminusTransactor) CreatePoolV1(opts *bind.TransactOpts, _capacity *big.Int, _transferable bool, _burnable bool) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "createPoolV1", _capacity, _transferable, _burnable)
}

// CreatePoolV1 is a paid mutator transaction binding the contract method 0x3bad2d82.
//
// Solidity: function createPoolV1(uint256 _capacity, bool _transferable, bool _burnable) returns(uint256)
func (_Terminus *TerminusSession) CreatePoolV1(_capacity *big.Int, _transferable bool, _burnable bool) (*types.Transaction, error) {
	return _Terminus.Contract.CreatePoolV1(&_Terminus.TransactOpts, _capacity, _transferable, _burnable)
}

// CreatePoolV1 is a paid mutator transaction binding the contract method 0x3bad2d82.
//
// Solidity: function createPoolV1(uint256 _capacity, bool _transferable, bool _burnable) returns(uint256)
func (_Terminus *TerminusTransactorSession) CreatePoolV1(_capacity *big.Int, _transferable bool, _burnable bool) (*types.Transaction, error) {
	return _Terminus.Contract.CreatePoolV1(&_Terminus.TransactOpts, _capacity, _transferable, _burnable)
}

// CreateSimplePool is a paid mutator transaction binding the contract method 0xb507ef52.
//
// Solidity: function createSimplePool(uint256 _capacity) returns(uint256)
func (_Terminus *TerminusTransactor) CreateSimplePool(opts *bind.TransactOpts, _capacity *big.Int) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "createSimplePool", _capacity)
}

// CreateSimplePool is a paid mutator transaction binding the contract method 0xb507ef52.
//
// Solidity: function createSimplePool(uint256 _capacity) returns(uint256)
func (_Terminus *TerminusSession) CreateSimplePool(_capacity *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.CreateSimplePool(&_Terminus.TransactOpts, _capacity)
}

// CreateSimplePool is a paid mutator transaction binding the contract method 0xb507ef52.
//
// Solidity: function createSimplePool(uint256 _capacity) returns(uint256)
func (_Terminus *TerminusTransactorSession) CreateSimplePool(_capacity *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.CreateSimplePool(&_Terminus.TransactOpts, _capacity)
}

// Mint is a paid mutator transaction binding the contract method 0x731133e9.
//
// Solidity: function mint(address to, uint256 poolID, uint256 amount, bytes data) returns()
func (_Terminus *TerminusTransactor) Mint(opts *bind.TransactOpts, to common.Address, poolID *big.Int, amount *big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "mint", to, poolID, amount, data)
}

// Mint is a paid mutator transaction binding the contract method 0x731133e9.
//
// Solidity: function mint(address to, uint256 poolID, uint256 amount, bytes data) returns()
func (_Terminus *TerminusSession) Mint(to common.Address, poolID *big.Int, amount *big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.Mint(&_Terminus.TransactOpts, to, poolID, amount, data)
}

// Mint is a paid mutator transaction binding the contract method 0x731133e9.
//
// Solidity: function mint(address to, uint256 poolID, uint256 amount, bytes data) returns()
func (_Terminus *TerminusTransactorSession) Mint(to common.Address, poolID *big.Int, amount *big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.Mint(&_Terminus.TransactOpts, to, poolID, amount, data)
}

// MintBatch is a paid mutator transaction binding the contract method 0x1f7fdffa.
//
// Solidity: function mintBatch(address to, uint256[] poolIDs, uint256[] amounts, bytes data) returns()
func (_Terminus *TerminusTransactor) MintBatch(opts *bind.TransactOpts, to common.Address, poolIDs []*big.Int, amounts []*big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "mintBatch", to, poolIDs, amounts, data)
}

// MintBatch is a paid mutator transaction binding the contract method 0x1f7fdffa.
//
// Solidity: function mintBatch(address to, uint256[] poolIDs, uint256[] amounts, bytes data) returns()
func (_Terminus *TerminusSession) MintBatch(to common.Address, poolIDs []*big.Int, amounts []*big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.MintBatch(&_Terminus.TransactOpts, to, poolIDs, amounts, data)
}

// MintBatch is a paid mutator transaction binding the contract method 0x1f7fdffa.
//
// Solidity: function mintBatch(address to, uint256[] poolIDs, uint256[] amounts, bytes data) returns()
func (_Terminus *TerminusTransactorSession) MintBatch(to common.Address, poolIDs []*big.Int, amounts []*big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.MintBatch(&_Terminus.TransactOpts, to, poolIDs, amounts, data)
}

// PoolMintBatch is a paid mutator transaction binding the contract method 0x21adca96.
//
// Solidity: function poolMintBatch(uint256 id, address[] toAddresses, uint256[] amounts) returns()
func (_Terminus *TerminusTransactor) PoolMintBatch(opts *bind.TransactOpts, id *big.Int, toAddresses []common.Address, amounts []*big.Int) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "poolMintBatch", id, toAddresses, amounts)
}

// PoolMintBatch is a paid mutator transaction binding the contract method 0x21adca96.
//
// Solidity: function poolMintBatch(uint256 id, address[] toAddresses, uint256[] amounts) returns()
func (_Terminus *TerminusSession) PoolMintBatch(id *big.Int, toAddresses []common.Address, amounts []*big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.PoolMintBatch(&_Terminus.TransactOpts, id, toAddresses, amounts)
}

// PoolMintBatch is a paid mutator transaction binding the contract method 0x21adca96.
//
// Solidity: function poolMintBatch(uint256 id, address[] toAddresses, uint256[] amounts) returns()
func (_Terminus *TerminusTransactorSession) PoolMintBatch(id *big.Int, toAddresses []common.Address, amounts []*big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.PoolMintBatch(&_Terminus.TransactOpts, id, toAddresses, amounts)
}

// SafeBatchTransferFrom is a paid mutator transaction binding the contract method 0x2eb2c2d6.
//
// Solidity: function safeBatchTransferFrom(address from, address to, uint256[] ids, uint256[] amounts, bytes data) returns()
func (_Terminus *TerminusTransactor) SafeBatchTransferFrom(opts *bind.TransactOpts, from common.Address, to common.Address, ids []*big.Int, amounts []*big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "safeBatchTransferFrom", from, to, ids, amounts, data)
}

// SafeBatchTransferFrom is a paid mutator transaction binding the contract method 0x2eb2c2d6.
//
// Solidity: function safeBatchTransferFrom(address from, address to, uint256[] ids, uint256[] amounts, bytes data) returns()
func (_Terminus *TerminusSession) SafeBatchTransferFrom(from common.Address, to common.Address, ids []*big.Int, amounts []*big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.SafeBatchTransferFrom(&_Terminus.TransactOpts, from, to, ids, amounts, data)
}

// SafeBatchTransferFrom is a paid mutator transaction binding the contract method 0x2eb2c2d6.
//
// Solidity: function safeBatchTransferFrom(address from, address to, uint256[] ids, uint256[] amounts, bytes data) returns()
func (_Terminus *TerminusTransactorSession) SafeBatchTransferFrom(from common.Address, to common.Address, ids []*big.Int, amounts []*big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.SafeBatchTransferFrom(&_Terminus.TransactOpts, from, to, ids, amounts, data)
}

// SafeTransferFrom is a paid mutator transaction binding the contract method 0xf242432a.
//
// Solidity: function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes data) returns()
func (_Terminus *TerminusTransactor) SafeTransferFrom(opts *bind.TransactOpts, from common.Address, to common.Address, id *big.Int, amount *big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "safeTransferFrom", from, to, id, amount, data)
}

// SafeTransferFrom is a paid mutator transaction binding the contract method 0xf242432a.
//
// Solidity: function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes data) returns()
func (_Terminus *TerminusSession) SafeTransferFrom(from common.Address, to common.Address, id *big.Int, amount *big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.SafeTransferFrom(&_Terminus.TransactOpts, from, to, id, amount, data)
}

// SafeTransferFrom is a paid mutator transaction binding the contract method 0xf242432a.
//
// Solidity: function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes data) returns()
func (_Terminus *TerminusTransactorSession) SafeTransferFrom(from common.Address, to common.Address, id *big.Int, amount *big.Int, data []byte) (*types.Transaction, error) {
	return _Terminus.Contract.SafeTransferFrom(&_Terminus.TransactOpts, from, to, id, amount, data)
}

// SetApprovalForAll is a paid mutator transaction binding the contract method 0xa22cb465.
//
// Solidity: function setApprovalForAll(address operator, bool approved) returns()
func (_Terminus *TerminusTransactor) SetApprovalForAll(opts *bind.TransactOpts, operator common.Address, approved bool) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "setApprovalForAll", operator, approved)
}

// SetApprovalForAll is a paid mutator transaction binding the contract method 0xa22cb465.
//
// Solidity: function setApprovalForAll(address operator, bool approved) returns()
func (_Terminus *TerminusSession) SetApprovalForAll(operator common.Address, approved bool) (*types.Transaction, error) {
	return _Terminus.Contract.SetApprovalForAll(&_Terminus.TransactOpts, operator, approved)
}

// SetApprovalForAll is a paid mutator transaction binding the contract method 0xa22cb465.
//
// Solidity: function setApprovalForAll(address operator, bool approved) returns()
func (_Terminus *TerminusTransactorSession) SetApprovalForAll(operator common.Address, approved bool) (*types.Transaction, error) {
	return _Terminus.Contract.SetApprovalForAll(&_Terminus.TransactOpts, operator, approved)
}

// SetContractURI is a paid mutator transaction binding the contract method 0x938e3d7b.
//
// Solidity: function setContractURI(string _contractURI) returns()
func (_Terminus *TerminusTransactor) SetContractURI(opts *bind.TransactOpts, _contractURI string) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "setContractURI", _contractURI)
}

// SetContractURI is a paid mutator transaction binding the contract method 0x938e3d7b.
//
// Solidity: function setContractURI(string _contractURI) returns()
func (_Terminus *TerminusSession) SetContractURI(_contractURI string) (*types.Transaction, error) {
	return _Terminus.Contract.SetContractURI(&_Terminus.TransactOpts, _contractURI)
}

// SetContractURI is a paid mutator transaction binding the contract method 0x938e3d7b.
//
// Solidity: function setContractURI(string _contractURI) returns()
func (_Terminus *TerminusTransactorSession) SetContractURI(_contractURI string) (*types.Transaction, error) {
	return _Terminus.Contract.SetContractURI(&_Terminus.TransactOpts, _contractURI)
}

// SetPaymentToken is a paid mutator transaction binding the contract method 0x6a326ab1.
//
// Solidity: function setPaymentToken(address newPaymentToken) returns()
func (_Terminus *TerminusTransactor) SetPaymentToken(opts *bind.TransactOpts, newPaymentToken common.Address) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "setPaymentToken", newPaymentToken)
}

// SetPaymentToken is a paid mutator transaction binding the contract method 0x6a326ab1.
//
// Solidity: function setPaymentToken(address newPaymentToken) returns()
func (_Terminus *TerminusSession) SetPaymentToken(newPaymentToken common.Address) (*types.Transaction, error) {
	return _Terminus.Contract.SetPaymentToken(&_Terminus.TransactOpts, newPaymentToken)
}

// SetPaymentToken is a paid mutator transaction binding the contract method 0x6a326ab1.
//
// Solidity: function setPaymentToken(address newPaymentToken) returns()
func (_Terminus *TerminusTransactorSession) SetPaymentToken(newPaymentToken common.Address) (*types.Transaction, error) {
	return _Terminus.Contract.SetPaymentToken(&_Terminus.TransactOpts, newPaymentToken)
}

// SetPoolBasePrice is a paid mutator transaction binding the contract method 0x78cf2e84.
//
// Solidity: function setPoolBasePrice(uint256 newBasePrice) returns()
func (_Terminus *TerminusTransactor) SetPoolBasePrice(opts *bind.TransactOpts, newBasePrice *big.Int) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "setPoolBasePrice", newBasePrice)
}

// SetPoolBasePrice is a paid mutator transaction binding the contract method 0x78cf2e84.
//
// Solidity: function setPoolBasePrice(uint256 newBasePrice) returns()
func (_Terminus *TerminusSession) SetPoolBasePrice(newBasePrice *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.SetPoolBasePrice(&_Terminus.TransactOpts, newBasePrice)
}

// SetPoolBasePrice is a paid mutator transaction binding the contract method 0x78cf2e84.
//
// Solidity: function setPoolBasePrice(uint256 newBasePrice) returns()
func (_Terminus *TerminusTransactorSession) SetPoolBasePrice(newBasePrice *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.SetPoolBasePrice(&_Terminus.TransactOpts, newBasePrice)
}

// SetPoolController is a paid mutator transaction binding the contract method 0xdc55d0b2.
//
// Solidity: function setPoolController(uint256 poolID, address newController) returns()
func (_Terminus *TerminusTransactor) SetPoolController(opts *bind.TransactOpts, poolID *big.Int, newController common.Address) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "setPoolController", poolID, newController)
}

// SetPoolController is a paid mutator transaction binding the contract method 0xdc55d0b2.
//
// Solidity: function setPoolController(uint256 poolID, address newController) returns()
func (_Terminus *TerminusSession) SetPoolController(poolID *big.Int, newController common.Address) (*types.Transaction, error) {
	return _Terminus.Contract.SetPoolController(&_Terminus.TransactOpts, poolID, newController)
}

// SetPoolController is a paid mutator transaction binding the contract method 0xdc55d0b2.
//
// Solidity: function setPoolController(uint256 poolID, address newController) returns()
func (_Terminus *TerminusTransactorSession) SetPoolController(poolID *big.Int, newController common.Address) (*types.Transaction, error) {
	return _Terminus.Contract.SetPoolController(&_Terminus.TransactOpts, poolID, newController)
}

// SetURI is a paid mutator transaction binding the contract method 0x862440e2.
//
// Solidity: function setURI(uint256 poolID, string poolURI) returns()
func (_Terminus *TerminusTransactor) SetURI(opts *bind.TransactOpts, poolID *big.Int, poolURI string) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "setURI", poolID, poolURI)
}

// SetURI is a paid mutator transaction binding the contract method 0x862440e2.
//
// Solidity: function setURI(uint256 poolID, string poolURI) returns()
func (_Terminus *TerminusSession) SetURI(poolID *big.Int, poolURI string) (*types.Transaction, error) {
	return _Terminus.Contract.SetURI(&_Terminus.TransactOpts, poolID, poolURI)
}

// SetURI is a paid mutator transaction binding the contract method 0x862440e2.
//
// Solidity: function setURI(uint256 poolID, string poolURI) returns()
func (_Terminus *TerminusTransactorSession) SetURI(poolID *big.Int, poolURI string) (*types.Transaction, error) {
	return _Terminus.Contract.SetURI(&_Terminus.TransactOpts, poolID, poolURI)
}

// WithdrawPayments is a paid mutator transaction binding the contract method 0x0e7afec5.
//
// Solidity: function withdrawPayments(address toAddress, uint256 amount) returns()
func (_Terminus *TerminusTransactor) WithdrawPayments(opts *bind.TransactOpts, toAddress common.Address, amount *big.Int) (*types.Transaction, error) {
	return _Terminus.contract.Transact(opts, "withdrawPayments", toAddress, amount)
}

// WithdrawPayments is a paid mutator transaction binding the contract method 0x0e7afec5.
//
// Solidity: function withdrawPayments(address toAddress, uint256 amount) returns()
func (_Terminus *TerminusSession) WithdrawPayments(toAddress common.Address, amount *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.WithdrawPayments(&_Terminus.TransactOpts, toAddress, amount)
}

// WithdrawPayments is a paid mutator transaction binding the contract method 0x0e7afec5.
//
// Solidity: function withdrawPayments(address toAddress, uint256 amount) returns()
func (_Terminus *TerminusTransactorSession) WithdrawPayments(toAddress common.Address, amount *big.Int) (*types.Transaction, error) {
	return _Terminus.Contract.WithdrawPayments(&_Terminus.TransactOpts, toAddress, amount)
}

// TerminusApprovalForAllIterator is returned from FilterApprovalForAll and is used to iterate over the raw logs and unpacked data for ApprovalForAll events raised by the Terminus contract.
type TerminusApprovalForAllIterator struct {
	Event *TerminusApprovalForAll // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *TerminusApprovalForAllIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(TerminusApprovalForAll)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(TerminusApprovalForAll)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *TerminusApprovalForAllIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *TerminusApprovalForAllIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// TerminusApprovalForAll represents a ApprovalForAll event raised by the Terminus contract.
type TerminusApprovalForAll struct {
	Account  common.Address
	Operator common.Address
	Approved bool
	Raw      types.Log // Blockchain specific contextual infos
}

// FilterApprovalForAll is a free log retrieval operation binding the contract event 0x17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31.
//
// Solidity: event ApprovalForAll(address indexed account, address indexed operator, bool approved)
func (_Terminus *TerminusFilterer) FilterApprovalForAll(opts *bind.FilterOpts, account []common.Address, operator []common.Address) (*TerminusApprovalForAllIterator, error) {

	var accountRule []interface{}
	for _, accountItem := range account {
		accountRule = append(accountRule, accountItem)
	}
	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}

	logs, sub, err := _Terminus.contract.FilterLogs(opts, "ApprovalForAll", accountRule, operatorRule)
	if err != nil {
		return nil, err
	}
	return &TerminusApprovalForAllIterator{contract: _Terminus.contract, event: "ApprovalForAll", logs: logs, sub: sub}, nil
}

// WatchApprovalForAll is a free log subscription operation binding the contract event 0x17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31.
//
// Solidity: event ApprovalForAll(address indexed account, address indexed operator, bool approved)
func (_Terminus *TerminusFilterer) WatchApprovalForAll(opts *bind.WatchOpts, sink chan<- *TerminusApprovalForAll, account []common.Address, operator []common.Address) (event.Subscription, error) {

	var accountRule []interface{}
	for _, accountItem := range account {
		accountRule = append(accountRule, accountItem)
	}
	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}

	logs, sub, err := _Terminus.contract.WatchLogs(opts, "ApprovalForAll", accountRule, operatorRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(TerminusApprovalForAll)
				if err := _Terminus.contract.UnpackLog(event, "ApprovalForAll", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseApprovalForAll is a log parse operation binding the contract event 0x17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31.
//
// Solidity: event ApprovalForAll(address indexed account, address indexed operator, bool approved)
func (_Terminus *TerminusFilterer) ParseApprovalForAll(log types.Log) (*TerminusApprovalForAll, error) {
	event := new(TerminusApprovalForAll)
	if err := _Terminus.contract.UnpackLog(event, "ApprovalForAll", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// TerminusPoolMintBatchIterator is returned from FilterPoolMintBatch and is used to iterate over the raw logs and unpacked data for PoolMintBatch events raised by the Terminus contract.
type TerminusPoolMintBatchIterator struct {
	Event *TerminusPoolMintBatch // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *TerminusPoolMintBatchIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(TerminusPoolMintBatch)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(TerminusPoolMintBatch)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *TerminusPoolMintBatchIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *TerminusPoolMintBatchIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// TerminusPoolMintBatch represents a PoolMintBatch event raised by the Terminus contract.
type TerminusPoolMintBatch struct {
	Id          *big.Int
	Operator    common.Address
	From        common.Address
	ToAddresses []common.Address
	Amounts     []*big.Int
	Raw         types.Log // Blockchain specific contextual infos
}

// FilterPoolMintBatch is a free log retrieval operation binding the contract event 0xba62777935b5e992de16a785941daef9f13517ff268a40563288072025b50238.
//
// Solidity: event PoolMintBatch(uint256 indexed id, address indexed operator, address from, address[] toAddresses, uint256[] amounts)
func (_Terminus *TerminusFilterer) FilterPoolMintBatch(opts *bind.FilterOpts, id []*big.Int, operator []common.Address) (*TerminusPoolMintBatchIterator, error) {

	var idRule []interface{}
	for _, idItem := range id {
		idRule = append(idRule, idItem)
	}
	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}

	logs, sub, err := _Terminus.contract.FilterLogs(opts, "PoolMintBatch", idRule, operatorRule)
	if err != nil {
		return nil, err
	}
	return &TerminusPoolMintBatchIterator{contract: _Terminus.contract, event: "PoolMintBatch", logs: logs, sub: sub}, nil
}

// WatchPoolMintBatch is a free log subscription operation binding the contract event 0xba62777935b5e992de16a785941daef9f13517ff268a40563288072025b50238.
//
// Solidity: event PoolMintBatch(uint256 indexed id, address indexed operator, address from, address[] toAddresses, uint256[] amounts)
func (_Terminus *TerminusFilterer) WatchPoolMintBatch(opts *bind.WatchOpts, sink chan<- *TerminusPoolMintBatch, id []*big.Int, operator []common.Address) (event.Subscription, error) {

	var idRule []interface{}
	for _, idItem := range id {
		idRule = append(idRule, idItem)
	}
	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}

	logs, sub, err := _Terminus.contract.WatchLogs(opts, "PoolMintBatch", idRule, operatorRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(TerminusPoolMintBatch)
				if err := _Terminus.contract.UnpackLog(event, "PoolMintBatch", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParsePoolMintBatch is a log parse operation binding the contract event 0xba62777935b5e992de16a785941daef9f13517ff268a40563288072025b50238.
//
// Solidity: event PoolMintBatch(uint256 indexed id, address indexed operator, address from, address[] toAddresses, uint256[] amounts)
func (_Terminus *TerminusFilterer) ParsePoolMintBatch(log types.Log) (*TerminusPoolMintBatch, error) {
	event := new(TerminusPoolMintBatch)
	if err := _Terminus.contract.UnpackLog(event, "PoolMintBatch", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// TerminusTransferBatchIterator is returned from FilterTransferBatch and is used to iterate over the raw logs and unpacked data for TransferBatch events raised by the Terminus contract.
type TerminusTransferBatchIterator struct {
	Event *TerminusTransferBatch // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *TerminusTransferBatchIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(TerminusTransferBatch)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(TerminusTransferBatch)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *TerminusTransferBatchIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *TerminusTransferBatchIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// TerminusTransferBatch represents a TransferBatch event raised by the Terminus contract.
type TerminusTransferBatch struct {
	Operator common.Address
	From     common.Address
	To       common.Address
	Ids      []*big.Int
	Values   []*big.Int
	Raw      types.Log // Blockchain specific contextual infos
}

// FilterTransferBatch is a free log retrieval operation binding the contract event 0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb.
//
// Solidity: event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values)
func (_Terminus *TerminusFilterer) FilterTransferBatch(opts *bind.FilterOpts, operator []common.Address, from []common.Address, to []common.Address) (*TerminusTransferBatchIterator, error) {

	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}
	var fromRule []interface{}
	for _, fromItem := range from {
		fromRule = append(fromRule, fromItem)
	}
	var toRule []interface{}
	for _, toItem := range to {
		toRule = append(toRule, toItem)
	}

	logs, sub, err := _Terminus.contract.FilterLogs(opts, "TransferBatch", operatorRule, fromRule, toRule)
	if err != nil {
		return nil, err
	}
	return &TerminusTransferBatchIterator{contract: _Terminus.contract, event: "TransferBatch", logs: logs, sub: sub}, nil
}

// WatchTransferBatch is a free log subscription operation binding the contract event 0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb.
//
// Solidity: event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values)
func (_Terminus *TerminusFilterer) WatchTransferBatch(opts *bind.WatchOpts, sink chan<- *TerminusTransferBatch, operator []common.Address, from []common.Address, to []common.Address) (event.Subscription, error) {

	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}
	var fromRule []interface{}
	for _, fromItem := range from {
		fromRule = append(fromRule, fromItem)
	}
	var toRule []interface{}
	for _, toItem := range to {
		toRule = append(toRule, toItem)
	}

	logs, sub, err := _Terminus.contract.WatchLogs(opts, "TransferBatch", operatorRule, fromRule, toRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(TerminusTransferBatch)
				if err := _Terminus.contract.UnpackLog(event, "TransferBatch", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseTransferBatch is a log parse operation binding the contract event 0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb.
//
// Solidity: event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values)
func (_Terminus *TerminusFilterer) ParseTransferBatch(log types.Log) (*TerminusTransferBatch, error) {
	event := new(TerminusTransferBatch)
	if err := _Terminus.contract.UnpackLog(event, "TransferBatch", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// TerminusTransferSingleIterator is returned from FilterTransferSingle and is used to iterate over the raw logs and unpacked data for TransferSingle events raised by the Terminus contract.
type TerminusTransferSingleIterator struct {
	Event *TerminusTransferSingle // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *TerminusTransferSingleIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(TerminusTransferSingle)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(TerminusTransferSingle)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *TerminusTransferSingleIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *TerminusTransferSingleIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// TerminusTransferSingle represents a TransferSingle event raised by the Terminus contract.
type TerminusTransferSingle struct {
	Operator common.Address
	From     common.Address
	To       common.Address
	Id       *big.Int
	Value    *big.Int
	Raw      types.Log // Blockchain specific contextual infos
}

// FilterTransferSingle is a free log retrieval operation binding the contract event 0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62.
//
// Solidity: event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value)
func (_Terminus *TerminusFilterer) FilterTransferSingle(opts *bind.FilterOpts, operator []common.Address, from []common.Address, to []common.Address) (*TerminusTransferSingleIterator, error) {

	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}
	var fromRule []interface{}
	for _, fromItem := range from {
		fromRule = append(fromRule, fromItem)
	}
	var toRule []interface{}
	for _, toItem := range to {
		toRule = append(toRule, toItem)
	}

	logs, sub, err := _Terminus.contract.FilterLogs(opts, "TransferSingle", operatorRule, fromRule, toRule)
	if err != nil {
		return nil, err
	}
	return &TerminusTransferSingleIterator{contract: _Terminus.contract, event: "TransferSingle", logs: logs, sub: sub}, nil
}

// WatchTransferSingle is a free log subscription operation binding the contract event 0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62.
//
// Solidity: event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value)
func (_Terminus *TerminusFilterer) WatchTransferSingle(opts *bind.WatchOpts, sink chan<- *TerminusTransferSingle, operator []common.Address, from []common.Address, to []common.Address) (event.Subscription, error) {

	var operatorRule []interface{}
	for _, operatorItem := range operator {
		operatorRule = append(operatorRule, operatorItem)
	}
	var fromRule []interface{}
	for _, fromItem := range from {
		fromRule = append(fromRule, fromItem)
	}
	var toRule []interface{}
	for _, toItem := range to {
		toRule = append(toRule, toItem)
	}

	logs, sub, err := _Terminus.contract.WatchLogs(opts, "TransferSingle", operatorRule, fromRule, toRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(TerminusTransferSingle)
				if err := _Terminus.contract.UnpackLog(event, "TransferSingle", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseTransferSingle is a log parse operation binding the contract event 0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62.
//
// Solidity: event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value)
func (_Terminus *TerminusFilterer) ParseTransferSingle(log types.Log) (*TerminusTransferSingle, error) {
	event := new(TerminusTransferSingle)
	if err := _Terminus.contract.UnpackLog(event, "TransferSingle", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// TerminusURIIterator is returned from FilterURI and is used to iterate over the raw logs and unpacked data for URI events raised by the Terminus contract.
type TerminusURIIterator struct {
	Event *TerminusURI // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *TerminusURIIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(TerminusURI)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(TerminusURI)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *TerminusURIIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *TerminusURIIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// TerminusURI represents a URI event raised by the Terminus contract.
type TerminusURI struct {
	Value string
	Id    *big.Int
	Raw   types.Log // Blockchain specific contextual infos
}

// FilterURI is a free log retrieval operation binding the contract event 0x6bb7ff708619ba0610cba295a58592e0451dee2622938c8755667688daf3529b.
//
// Solidity: event URI(string value, uint256 indexed id)
func (_Terminus *TerminusFilterer) FilterURI(opts *bind.FilterOpts, id []*big.Int) (*TerminusURIIterator, error) {

	var idRule []interface{}
	for _, idItem := range id {
		idRule = append(idRule, idItem)
	}

	logs, sub, err := _Terminus.contract.FilterLogs(opts, "URI", idRule)
	if err != nil {
		return nil, err
	}
	return &TerminusURIIterator{contract: _Terminus.contract, event: "URI", logs: logs, sub: sub}, nil
}

// WatchURI is a free log subscription operation binding the contract event 0x6bb7ff708619ba0610cba295a58592e0451dee2622938c8755667688daf3529b.
//
// Solidity: event URI(string value, uint256 indexed id)
func (_Terminus *TerminusFilterer) WatchURI(opts *bind.WatchOpts, sink chan<- *TerminusURI, id []*big.Int) (event.Subscription, error) {

	var idRule []interface{}
	for _, idItem := range id {
		idRule = append(idRule, idItem)
	}

	logs, sub, err := _Terminus.contract.WatchLogs(opts, "URI", idRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(TerminusURI)
				if err := _Terminus.contract.UnpackLog(event, "URI", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseURI is a log parse operation binding the contract event 0x6bb7ff708619ba0610cba295a58592e0451dee2622938c8755667688daf3529b.
//
// Solidity: event URI(string value, uint256 indexed id)
func (_Terminus *TerminusFilterer) ParseURI(log types.Log) (*TerminusURI, error) {
	event := new(TerminusURI)
	if err := _Terminus.contract.UnpackLog(event, "URI", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}
