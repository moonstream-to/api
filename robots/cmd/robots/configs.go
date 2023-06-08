/*
Configurations for robots server.
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
)

var (
	NODEBALANCER_ACCESS_ID    = os.Getenv("ENGINE_NODEBALANCER_ACCESS_ID")
	MUMBAI_WEB3_PROVIDER_URI  = os.Getenv("MOONSTREAM_MUMBAI_WEB3_PROVIDER_URI")
	POLYGON_WEB3_PROVIDER_URI = os.Getenv("MOONSTREAM_POLYGON_WEB3_PROVIDER_URI")
	WYRM_WEB3_PROVIDER_URI = os.Getenv("MOONSTREAM_WYRM_WEB3_PROVIDER_URI")

	JOURNAL_SEARCH_BATCH_SIZE = 20

	ROBOTS_SIGNER_SECRETS_DIR_PATH = os.Getenv("ENGINE_ROBOTS_SECRETS_DIR")

	HUMBUG_REPORTER_ROBOTS_HEARTBEAT_TOKEN = os.Getenv("HUMBUG_REPORTER_ROBOTS_HEARTBEAT_TOKEN")
)

type RobotsConfig struct {
	CollectionId           string `json:"collection_id"`
	SignerKeyfileName      string `json:"signer_keyfile_name"`
	SignerPasswordFileName string `json:"signer_password_file_name"`
	TerminusPoolId         int64  `json:"terminus_pool_id"`
	Blockchain             string `json:"blockchain"`
	TerminusAddress        string `json:"terminus_address"`
	ValueToClaim           int64  `json:"value_to_claim"`
	MaxValueToClaim        int64  `json:"max_value_to_claim"`
}

func LoadConfig(configPath string) (*[]RobotsConfig, error) {
	rawBytes, err := ioutil.ReadFile(configPath)
	if err != nil {
		return nil, err
	}
	robotsConfigs := &[]RobotsConfig{}
	err = json.Unmarshal(rawBytes, robotsConfigs)
	if err != nil {
		return nil, err
	}
	return robotsConfigs, nil
}

type ConfigPlacement struct {
	ConfigDirPath   string
	ConfigDirExists bool

	ConfigPath   string
	ConfigExists bool
}

// CheckPathExists checks if path to file exists
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

func PrepareConfigPlacement(providedPath string) (*ConfigPlacement, error) {
	var configDirPath, configPath string
	if providedPath == "" {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			return nil, fmt.Errorf("Unable to find user home directory, %v", err)
		}
		configDirPath = fmt.Sprintf("%s/.robots", homeDir)
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

	configPlacement := &ConfigPlacement{
		ConfigDirPath:   configDirPath,
		ConfigDirExists: configDirPathExists,

		ConfigPath:   configPath,
		ConfigExists: configPathExists,
	}

	return configPlacement, nil
}

// Generates empty list of robots configuration
func GenerateDefaultConfig(config *ConfigPlacement) error {
	if !config.ConfigDirExists {
		if err := os.MkdirAll(config.ConfigDirPath, os.ModePerm); err != nil {
			return fmt.Errorf("Unable to create directory, %v", err)
		}
		log.Printf("Config directory created at: %s", config.ConfigDirPath)
	}

	if !config.ConfigExists {
		tempConfig := []RobotsConfig{}
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
