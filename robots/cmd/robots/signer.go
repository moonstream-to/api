package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/accounts/keystore"
	"github.com/ethereum/go-ethereum/common"
)

type SignerInstance struct {
	Address    common.Address
	PrivateKey *keystore.Key
}

// initializeSigner parse secrets directory with keyfile and passfile,
// then opens keyfile with password to privateKey
func initializeSigner(keyfileName, passfileName string) (*SignerInstance, error) {
	if ROBOTS_SIGNER_SECRETS_DIR_PATH == "" {
		return nil, errors.New("Directory with signer secrets not set")
	}

	keyfilePath := fmt.Sprintf("%s/%s", ROBOTS_SIGNER_SECRETS_DIR_PATH, keyfileName)
	keyfilePasswordPath := fmt.Sprintf("%s/%s", ROBOTS_SIGNER_SECRETS_DIR_PATH, passfileName)

	passfile, err := ioutil.ReadFile(keyfilePasswordPath)
	if err != nil {
		return nil, err
	}
	passfile_lines := strings.Split(string(passfile), "\n")
	password := passfile_lines[0]

	keyfile, err := ioutil.ReadFile(keyfilePath)
	if err != nil {
		return nil, err
	}

	privateKey, err := keystore.DecryptKey(keyfile, password)
	if err != nil {
		return nil, err
	}

	signer := SignerInstance{
		Address:    privateKey.Address,
		PrivateKey: privateKey,
	}

	return &signer, nil
}

func (s *SignerInstance) CreateTransactor(network NetworkInstance) (*bind.TransactOpts, error) {
	auth, err := bind.NewKeyedTransactorWithChainID(s.PrivateKey.PrivateKey, network.ChainID)
	if err != nil {
		return nil, err
	}
	// auth.Nonce = big.NewInt(int64(nonce))
	// auth.Value = big.NewInt(0)
	// auth.GasLimit = uint64(300000)
	// auth.GasPrice = gasPrice

	return auth, nil
}
