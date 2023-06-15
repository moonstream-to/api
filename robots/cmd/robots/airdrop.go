package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"math/big"
	"sync"
	"sync/atomic"
	"time"

	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/google/uuid"
)

type RobotInstance struct {
	ValueToClaim    int64
	MaxValueToClaim int64

	ContractTerminusInstance ContractTerminusInstance
	EntityInstance           EntityInstance
	NetworkInstance          NetworkInstance
	SignerInstance           SignerInstance

	MintCounter int64
}

func Airdrop(configs *[]RobotsConfig) {
	sessionID := uuid.New().String()
	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err := humbug.CreateHumbugReporter(consent, "moonstream-robots", sessionID, HUMBUG_REPORTER_ROBOTS_HEARTBEAT_TOKEN)
	if err != nil {
		log.Printf("Unable to specify humbug heartbeat reporter, %v", err)
	}
	// Record system information
	reporter.Publish(humbug.SystemReport())

	var robots []RobotInstance

	// Configure networks
	networks, err := InitializeNetworks()
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Initialized configuration of network endpoints and chain IDs")

	ctx := context.Background()
	for _, config := range *configs {
		robot := RobotInstance{
			ValueToClaim:    config.ValueToClaim,
			MaxValueToClaim: config.MaxValueToClaim,
			MintCounter:     0, // TODO(kompotkot): Fetch minted number from blockchain
		}

		// Configure network client
		network := networks[config.Blockchain]
		client, err := GenDialRpcClient(network.Endpoint)
		if err != nil {
			log.Fatal(err)
		}
		robot.NetworkInstance = NetworkInstance{
			Blockchain: config.Blockchain,
			Endpoint:   network.Endpoint,
			ChainID:    network.ChainID,

			Client: client,
		}
		log.Printf("Initialized configuration of JSON RPC network client for %s blockchain", config.Blockchain)

		// Fetch required opts
		err = robot.NetworkInstance.FetchSuggestedGasPrice(ctx)
		if err != nil {
			log.Fatal(err)
		}

		// Define contract instance
		contractAddress := GetTerminusContractAddress(config.TerminusAddress)
		contractTerminusInstance, err := InitializeTerminusContractInstance(client, contractAddress)
		if err != nil {
			log.Fatal(err)
		}
		robot.ContractTerminusInstance = ContractTerminusInstance{
			Address:        contractAddress,
			Instance:       contractTerminusInstance,
			TerminusPoolId: config.TerminusPoolId,
		}
		log.Printf("Initialized configuration of terminus contract instance for %s blockchain", config.Blockchain)

		// Configure entity client
		entityInstance, err := InitializeEntityInstance(config.CollectionId)
		if err != nil {
			log.Fatal(err)
		}
		robot.EntityInstance = *entityInstance
		log.Printf("Initialized configuration of entity client for '%s' collection", robot.EntityInstance.CollectionId)

		// Configure signer
		signer, err := initializeSigner(config.SignerKeyfileName, config.SignerPasswordFileName)
		if err != nil {
			log.Fatal(err)
		}
		robot.SignerInstance = *signer
		log.Printf("Initialized configuration of signer %s", robot.SignerInstance.Address.String())

		robots = append(robots, robot)
	}

	var wg sync.WaitGroup
	for idx, robot := range robots {
		wg.Add(1)
		go robotRun(
			&wg,
			robot,
			reporter,
			idx,
		)
	}
	wg.Wait()
}

type RobotHeartBeatReport struct {
	CollectionId   string `json:"collection_id"`
	CollectionName string `json:"collection_name"`
	SignerAddress  string `json:"signer_address"`
	TerminusPoolId int64  `json:"terminus_pool_id"`
	Blockchain     string `json:"blockchain"`
	MintCounter    int64  `json:"mint_counter"`
}

// heartBeat prepares and send HeartBeat report for robot
func heartBeat(
	robot RobotInstance,
	reporter *humbug.HumbugReporter,
	idx int,
) {
	reportContent := []byte{}
	robotHeartBeatReport := &RobotHeartBeatReport{
		CollectionId:   robot.EntityInstance.CollectionId,
		CollectionName: robot.EntityInstance.CollectionName,
		SignerAddress:  robot.SignerInstance.Address.String(),
		TerminusPoolId: robot.ContractTerminusInstance.TerminusPoolId,
		Blockchain:     robot.NetworkInstance.Blockchain,
		MintCounter:    robot.MintCounter,
	}
	reportContent, err := json.Marshal(robotHeartBeatReport)
	if err != nil {
		log.Printf("Unable to prepare report content for HeartBeat %v", err)
	}
	heartBeatReport := humbug.Report{
		Title: fmt.Sprintf("Robot %d HB - %s - %s", idx, robot.NetworkInstance.Blockchain, robot.EntityInstance.CollectionName),
		Tags: []string{
			fmt.Sprintf("index:%d", idx),
			fmt.Sprintf("blockchain:%s", robot.NetworkInstance.Blockchain),
			fmt.Sprintf("collection_id:%s", robot.EntityInstance.CollectionId),
			fmt.Sprintf("terminus_pool_id:%d", robot.ContractTerminusInstance.TerminusPoolId),
			fmt.Sprintf("signer_address:%s", robot.SignerInstance.Address.String()),
		},
		Content: string(reportContent),
	}
	reporter.Publish(heartBeatReport)
}

// robotRun represents of each robot instance for specific airdrop
func robotRun(
	wg *sync.WaitGroup,
	robot RobotInstance,
	reporter *humbug.HumbugReporter,
	idx int,
) {
	defer wg.Done()

	log.Printf(
		"Spawned robot %d for blockchain %s, signer %s, entity collection %s, pool %d",
		idx,
		robot.NetworkInstance.Blockchain,
		robot.SignerInstance.Address.String(),
		robot.EntityInstance.CollectionId,
		robot.ContractTerminusInstance.TerminusPoolId,
	)
	minSleepTime := 5
	maxSleepTime := 60
	timer := minSleepTime
	ticker := time.NewTicker(time.Duration(minSleepTime) * time.Second)

	for {
		select {
		case <-ticker.C:
			heartBeat(robot, reporter, idx)

			empty_addresses_len, err := airdropRun(&robot, idx)
			if err != nil {
				log.Printf("Robot %d - During AirdropRun an error occurred, err: %v", idx, err)
				timer = timer + 10
				ticker.Reset(time.Duration(timer) * time.Second)
				continue
			}
			if empty_addresses_len == 0 {
				timer = int(math.Min(float64(maxSleepTime), float64(timer+1)))
				ticker.Reset(time.Duration(timer) * time.Second)
				log.Printf("Robot %d - Sleeping for %d seconds because of no new empty addresses", idx, timer)
				continue
			}
			timer = int(math.Max(float64(minSleepTime), float64(timer-10)))
			ticker.Reset(time.Duration(timer) * time.Second)
		}
	}
}

type Claimant struct {
	EntityId string
	Address  string
}

func airdropRun(robot *RobotInstance, idx int) (int64, error) {
	status_code, search_data, err := robot.EntityInstance.FetchPublicSearchUntouched(JOURNAL_SEARCH_BATCH_SIZE)
	if err != nil {
		return 0, err
	}
	log.Printf("Robot %d - Received response %d from entities API for collection %s with %d results", idx, status_code, robot.EntityInstance.CollectionId, search_data.TotalResults)

	var claimants_len int64
	var claimants []Claimant
	for _, entity := range search_data.Entities {
		claimants = append(claimants, Claimant{
			EntityId: entity.EntityId,
			Address:  entity.Address,
		})
		claimants_len++
	}

	if claimants_len == 0 {
		return claimants_len, nil
	}

	// Fetch balances for addresses and update list
	balances, err := robot.ContractTerminusInstance.BalanceOfBatch(nil, claimants, robot.ContractTerminusInstance.TerminusPoolId)
	if err != nil {
		return 0, err
	}

	maxMintBigInt := big.NewInt(robot.MaxValueToClaim)
	var emptyClaimantsLen int64
	var emptyClaimants []Claimant
	for i, balance := range balances {
		// Allow to claim only if less then maxMintBigInt
		if balance.Cmp(maxMintBigInt) == -1 {
			emptyClaimants = append(emptyClaimants, claimants[i])
			emptyClaimantsLen++
		}
	}

	if emptyClaimantsLen > 0 {
		log.Printf("Robot %d - Ready to send tokens for %d addresses from collection %s", idx, emptyClaimantsLen, robot.EntityInstance.CollectionId)

		auth, err := robot.SignerInstance.CreateTransactor(robot.NetworkInstance)
		if err != nil {
			return emptyClaimantsLen, err
		}
		if robot.NetworkInstance.Blockchain == "wyrm" {
			auth.GasPrice = big.NewInt(0)
		}

		tx, err := robot.ContractTerminusInstance.PoolMintBatch(auth, emptyClaimants, robot.ValueToClaim)
		if err != nil {
			return emptyClaimantsLen, err
		}
		atomic.AddInt64(&robot.MintCounter, emptyClaimantsLen)
		log.Printf("Robot %d - Pending tx for PoolMintBatch on blockchain %s at pool ID %d: 0x%x", idx, robot.NetworkInstance.Blockchain, robot.ContractTerminusInstance.TerminusPoolId, tx.Hash())
	}

	var touched_entities int64
	for _, claimant := range claimants {
		_, _, err := robot.EntityInstance.TouchPublicEntity(claimant.EntityId, 10)
		if err != nil {
			log.Printf("Robot %d - Unable to touch entity with ID: %s for claimant: %s, err: %v", idx, claimant.EntityId, claimant.Address, err)
			continue
		}
		touched_entities++
	}
	log.Printf("Robot %d - Marked %d entities from %d claimants total", idx, touched_entities, claimants_len)

	return emptyClaimantsLen, nil
}
