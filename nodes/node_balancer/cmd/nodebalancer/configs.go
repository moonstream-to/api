/*
Configurations for load balancer server.
*/
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"
)

var (
	nodeConfigs []NodeConfig

	supportedBlockchains map[string]bool

	// Bugout and application configuration
	BUGOUT_AUTH_CALL_TIMEOUT = time.Second * 5
	NB_APPLICATION_ID        = os.Getenv("NB_APPLICATION_ID")
	NB_CONTROLLER_TOKEN      = os.Getenv("NB_CONTROLLER_TOKEN")
	NB_CONTROLLER_ACCESS_ID  = os.Getenv("NB_CONTROLLER_ACCESS_ID")

	NB_CONNECTION_RETRIES          = 2
	NB_CONNECTION_RETRIES_INTERVAL = time.Millisecond * 10
	NB_HEALTH_CHECK_INTERVAL       = time.Millisecond * 5000
	NB_HEALTH_CHECK_CALL_TIMEOUT   = time.Second * 2

	NB_CACHE_CLEANING_INTERVAL  = time.Second * 10
	NB_CACHE_ACCESS_ID_LIFETIME = int64(120)

	NB_MAX_COUNTER_NUMBER = uint64(10000000)

	// Client configuration
	NB_CLIENT_NODE_KEEP_ALIVE = int64(5)   // How long to store node in hot list for client in seconds
	NB_HIGHEST_BLOCK_SHIFT    = uint64(50) // Allowed shift to prefer node with most highest block

	NB_ACCESS_ID_HEADER   = os.Getenv("NB_ACCESS_ID_HEADER")
	NB_DATA_SOURCE_HEADER = os.Getenv("NB_DATA_SOURCE_HEADER")

	// Humbug configuration
	HUMBUG_REPORTER_NB_TOKEN = os.Getenv("HUMBUG_REPORTER_NB_TOKEN")

	// Database configuration
	MOONSTREAM_DB_URI_READ_ONLY         = os.Getenv("MOONSTREAM_DB_URI_READ_ONLY")
	MOONSTREAM_DB_MAX_IDLE_CONNS    int = 30
	MOONSTREAM_DB_CONN_MAX_LIFETIME     = 30 * time.Minute
)

func CheckEnvVarSet() {
	if NB_ACCESS_ID_HEADER == "" {
		NB_ACCESS_ID_HEADER = "x-node-balancer-access-id"
	}
	if NB_DATA_SOURCE_HEADER == "" {
		NB_DATA_SOURCE_HEADER = "x-node-balancer-data-source"
	}
}

// Nodes configuration
type NodeConfig struct {
	Blockchain string   `json:"blockchain"`
	Endpoint   string   `json:"endpoint"`
	Tags       []string `json:"tags"`
}

func LoadConfig(configPath string) error {
	rawBytes, err := ioutil.ReadFile(configPath)
	if err != nil {
		return err
	}
	nodeConfigsTemp := &[]NodeConfig{}
	err = json.Unmarshal(rawBytes, nodeConfigsTemp)
	if err != nil {
		return err
	}
	nodeConfigs = *nodeConfigsTemp
	return nil
}

type ConfigPlacement struct {
	ConfigDirPath   string
	ConfigDirExists bool

	ConfigPath   string
	ConfigExists bool
}

func CheckPathExists(path string) (bool, error) {
	var exists = true
	_, err := os.Stat(path)
	if err != nil {
		if os.IsNotExist(err) {
			exists = false
		} else {
			return exists, fmt.Errorf("Error due checking file path exists, err: %v", err)
		}
	}

	return exists, nil
}

func GetConfigPath(providedPath string) (*ConfigPlacement, error) {
	var configDirPath, configPath string
	if providedPath == "" {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			return nil, fmt.Errorf("Unable to find user home directory, %v", err)
		}
		configDirPath = fmt.Sprintf("%s/.nodebalancer", homeDir)
		configPath = fmt.Sprintf("%s/config.json", configDirPath)
	} else {
		configPath = strings.TrimSuffix(providedPath, "/")
		configDirPath = filepath.Dir(configPath)
	}

	configDirPathExists, err := CheckPathExists(configDirPath)
	if err != nil {
		return nil, err
	}
	configPathExists, err := CheckPathExists(configPath)
	if err != nil {
		return nil, err
	}

	config := &ConfigPlacement{
		ConfigDirPath:   configDirPath,
		ConfigDirExists: configDirPathExists,

		ConfigPath:   configPath,
		ConfigExists: configPathExists,
	}

	return config, nil
}

func GenerateDefaultConfig(config *ConfigPlacement) error {
	if !config.ConfigDirExists {
		if err := os.MkdirAll(config.ConfigDirPath, os.ModePerm); err != nil {
			return fmt.Errorf("Unable to create directory, %v", err)
		}
		log.Printf("Config directory created at: %s", config.ConfigDirPath)
	}

	if !config.ConfigExists {
		tempConfig := []NodeConfig{
			{Blockchain: "ethereum", Endpoint: "http://127.0.0.1:8545", Tags: []string{"local"}},
		}
		tempConfigJson, err := json.Marshal(tempConfig)
		if err != nil {
			return fmt.Errorf("Unable to marshal configuration data, err: %v", err)
		}
		err = ioutil.WriteFile(config.ConfigPath, tempConfigJson, os.ModePerm)
		if err != nil {
			return fmt.Errorf("Unable to write default config to file %s, err: %v", config.ConfigPath, err)
		}
		log.Printf("Created default configuration at %s", config.ConfigPath)
	}

	return nil
}
