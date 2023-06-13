package main

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	probes "github.com/moonstream-to/api/probes/pkg"
)

func RunService(configPath string) error {
	// Load configuration
	configPlacement, err := GetConfigPlacement(configPath)
	if err != nil {
		return err
	}

	if !configPlacement.ConfigExists {
		if err := GenerateDefaultConfig(configPlacement); err != nil {
			return err
		}
	} else {
		log.Printf("Loaded configuration from %s", configPlacement.ConfigPath)
	}

	serviceConfigs, totalWorkersNum, err := ReadConfig(configPlacement.ConfigPath)
	if err != nil {
		return fmt.Errorf("unable to read config, err: %v", err)
	}

	log.Printf("Loaded configurations of %d services with %d workers", len(*serviceConfigs), totalWorkersNum)

	var wg sync.WaitGroup
	for _, service := range *serviceConfigs {
		for _, worker := range service.Workers {
			wg.Add(1)
			go RunWorker(&wg, worker, service.Name, service.DbUri)
		}
	}
	wg.Wait()

	return nil
}

func RunWorker(wg *sync.WaitGroup, worker probes.ServiceWorker, serviceName, dbUri string) error {
	defer wg.Done()

	ctx := context.Background()

	dbPool, err := CreateDbPool(ctx, dbUri, "10s")
	if err != nil {
		log.Printf("[%s] [%s] - database connection error, err: %v", serviceName, worker.Name, err)
		return err
	}
	defer dbPool.Close()

	t := time.NewTicker(time.Duration(worker.Interval) * time.Second)
	for {
		select {
		case <-t.C:
			err = worker.ExecFunction(ctx, dbPool)
			if err != nil {
				log.Printf("[%s] [%s] - an error occurred during execution, err: %v", serviceName, worker.Name, err)
				return err
			}
		}
	}
}
