package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"

	probes "github.com/moonstream-to/api/probes/pkg"
	engine "github.com/moonstream-to/api/probes/pkg/engine"
)

var (
	DEFAULT_CONFIG_DIR_NAME  = ".probes"
	DEFAULT_CONFIG_FILE_NAME = "config.json"
)

// Workers configuration
type ServiceWorkersConfig struct {
	Name    string                 `json:"name"`
	DbUri   string                 `json:"db_uri"`
	Workers []probes.ServiceWorker `json:"workers"`
}

func ReadConfig(configPath string) (*[]ServiceWorkersConfig, int, error) {
	totalWorkersNum := 0

	rawBytes, err := ioutil.ReadFile(configPath)
	if err != nil {
		return nil, totalWorkersNum, err
	}
	serviceWorkersConfigTemp := &[]ServiceWorkersConfig{}
	err = json.Unmarshal(rawBytes, serviceWorkersConfigTemp)
	if err != nil {
		return nil, totalWorkersNum, err
	}

	var serviceWorkersConfig []ServiceWorkersConfig
	for _, service := range *serviceWorkersConfigTemp {
		serviceDbUri := os.Getenv(service.DbUri)
		if serviceDbUri == "" {
			return nil, totalWorkersNum, fmt.Errorf("unable to load database URI for service %s", service.Name)
		}

		var serviceWorkers []probes.ServiceWorker

		// Link worker function
		for w, worker := range service.Workers {
			switch service.Name {
			case "engine":
				for _, engineWorker := range engine.ENGINE_SUPPORTED_WORKERS {
					if worker.Name == engineWorker.Name {
						serviceWorkers = append(serviceWorkers, probes.ServiceWorker{
							Name:         worker.Name,
							Interval:     worker.Interval,
							ExecFunction: engineWorker.ExecFunction,
						})
						log.Printf("[%s] [%s] - Registered function", service.Name, worker.Name)
						totalWorkersNum++
						continue
					}
				}
				if worker.ExecFunction == nil {
					service.Workers = append(service.Workers[:w], service.Workers[w+1:]...)
					log.Printf("Function for worker %s at service %s not found, removed from the list", worker.Name, service.Name)
				}
			default:
				service.Workers = append(service.Workers[:w], service.Workers[w+1:]...)
				log.Printf("Unsupported %s service with %s worker from the list", worker.Name, service.Name)
			}
		}
		serviceWorkersConfig = append(serviceWorkersConfig, ServiceWorkersConfig{
			Name:    service.Name,
			DbUri:   serviceDbUri,
			Workers: serviceWorkers,
		})
	}

	return &serviceWorkersConfig, totalWorkersNum, nil
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
			return exists, fmt.Errorf("error due checking file path exists, err: %v", err)
		}
	}

	return exists, nil
}

func GetConfigPlacement(providedPath string) (*ConfigPlacement, error) {
	var configDirPath, configPath string
	if providedPath == "" {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			return nil, fmt.Errorf("unable to find user home directory, %v", err)
		}
		configDirPath = fmt.Sprintf("%s/%s", homeDir, DEFAULT_CONFIG_DIR_NAME)
		configPath = fmt.Sprintf("%s/%s", configDirPath, DEFAULT_CONFIG_FILE_NAME)
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

func GenerateDefaultConfig(config *ConfigPlacement) error {
	if !config.ConfigDirExists {
		if err := os.MkdirAll(config.ConfigDirPath, os.ModePerm); err != nil {
			return fmt.Errorf("unable to create directory, %v", err)
		}
		log.Printf("Config directory created at: %s", config.ConfigDirPath)
	}

	if !config.ConfigExists {
		tempConfig := []ServiceWorkersConfig{}
		tempConfigJson, err := json.Marshal(tempConfig)
		if err != nil {
			return fmt.Errorf("unable to marshal configuration data, err: %v", err)
		}
		err = ioutil.WriteFile(config.ConfigPath, tempConfigJson, os.ModePerm)
		if err != nil {
			return fmt.Errorf("unable to write default config to file %s, err: %v", config.ConfigPath, err)
		}
		log.Printf("Created default configuration at %s", config.ConfigPath)
	}

	return nil
}
