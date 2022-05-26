/*
Configurations for load balancer server.
*/
package configs

import (
	"fmt"
	"log"
	"os"
	"time"
)

var (
	// Bugout and application configuration
	BUGOUT_AUTH_URL          = os.Getenv("BUGOUT_AUTH_URL")
	BUGOUT_AUTH_CALL_TIMEOUT = time.Second * 5
	NB_APPLICATION_ID        = os.Getenv("NB_APPLICATION_ID")
	NB_CONTROLLER_TOKEN      = os.Getenv("NB_CONTROLLER_TOKEN")
	NB_CONTROLLER_ACCESS_ID  = os.Getenv("NB_CONTROLLER_ACCESS_ID")

	NB_CONNECTION_RETRIES          = 2
	NB_CONNECTION_RETRIES_INTERVAL = time.Millisecond * 10
	NB_HEALTH_CHECK_INTERVAL       = time.Second * 5
	NB_HEALTH_CHECK_CALL_TIMEOUT   = time.Second * 2

	// Client configuration
	NB_CLIENT_NODE_KEEP_ALIVE = int64(5) // How long to store node in hot list for client in seconds

	NB_ACCESS_ID_HEADER   = os.Getenv("NB_ACCESS_ID_HEADER")
	NB_DATA_SOURCE_HEADER = os.Getenv("NB_DATA_SOURCE_HEADER")

	// Humbug configuration
	HUMBUG_REPORTER_NB_TOKEN = os.Getenv("HUMBUG_REPORTER_NB_TOKEN")

	// Database configuration
	MOONSTREAM_DB_URI_READ_ONLY         = os.Getenv("MOONSTREAM_DB_URI_READ_ONLY")
	MOONSTREAM_DB_MAX_IDLE_CONNS    int = 30
	MOONSTREAM_DB_CONN_MAX_LIFETIME     = 30 * time.Minute
)

var MOONSTREAM_NODES_SERVER_PORT = os.Getenv("MOONSTREAM_NODES_SERVER_PORT")

func CheckEnvVarSet() {
	if NB_ACCESS_ID_HEADER == "" {
		NB_ACCESS_ID_HEADER = "x-node-balancer-access-id"
	}
	if NB_DATA_SOURCE_HEADER == "" {
		NB_DATA_SOURCE_HEADER = "x-node-balancer-data-source"
	}

	if MOONSTREAM_NODES_SERVER_PORT == "" {
		fmt.Println("Environment variable MOONSTREAM_NODES_SERVER_PORT not set")
		os.Exit(1)
	}
}

func GenerateDefaultConfig() string {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		fmt.Printf("Unable to find user home directory, %v", err)
		os.Exit(1)
	}

	configDirPath := fmt.Sprintf("%s/.nodebalancer", homeDir)
	configPath := fmt.Sprintf("%s/config.txt", configDirPath)

	err = os.MkdirAll(configDirPath, os.ModePerm)
	if err != nil {
		fmt.Printf("Unable to create directory, %v", err)
		os.Exit(1)
	}

	_, err = os.Stat(configPath)
	if err != nil {
		tempConfigB := []byte("ethereum,127.0.0.1,8545")
		err = os.WriteFile(configPath, tempConfigB, 0644)
		if err != nil {
			fmt.Printf("Unable to create directory, %v", err)
			os.Exit(1)
		}
		log.Printf("Config directory were not found, created default configuration at %s", configPath)
	}

	return configPath
}
