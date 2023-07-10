package main

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"
)

func RunService(configPaths []string) error {
	// Load configuration
	configs, err := ReadConfig(configPaths)
	if err != nil {
		return fmt.Errorf("unable to read config, err: %v", err)
	}

	log.Printf("Loaded configurations of %d application probes", len(*configs))

	var wg sync.WaitGroup
	for _, config := range *configs {
		wg.Add(1)
		go RunWorker(&wg, config)
	}
	wg.Wait()

	return nil
}

func RunWorker(wg *sync.WaitGroup, config ApplicationProbeConfig) error {
	defer wg.Done()

	ctx := context.Background()

	dbPool, err := CreateDbPool(ctx, config.DbUri, config.DbTimeout)
	if err != nil {
		log.Printf("[%s] [%s] - unable to establish connection with database, err: %v", config.Application, config.Probe.Name, err)
		return err
	}

	defer dbPool.Close()

	t := time.NewTicker(time.Duration(config.Probe.Interval) * time.Second)
	for {
		select {
		case <-t.C:
			err = config.Probe.ExecFunction(ctx, dbPool)
			if err != nil {
				log.Printf("[%s] [%s] - an error occurred during execution, err: %v", config.Application, config.Probe.Name, err)
				continue
			}
		}
	}
}
