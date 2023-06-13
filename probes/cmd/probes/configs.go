package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"

	probes "github.com/moonstream-to/api/probes/pkg"
	engine "github.com/moonstream-to/api/probes/pkg/engine"
)

// Application Probe configuration
type ApplicationProbeConfig struct {
	Application string `json:"application"`
	DbUri       string `json:"db_uri"`
	DbTimeout   string `json:"db_timeout"`

	Probe probes.ApplicationProbe `json:"probe"`
}

// ReadConfig parses list of configuration file paths to list of Application Probes configs
func ReadConfig(rawConfigPaths []string) (*[]ApplicationProbeConfig, error) {
	var configs []ApplicationProbeConfig
	for _, rawConfigPath := range rawConfigPaths {
		configPath := strings.TrimSuffix(rawConfigPath, "/")
		_, err := os.Stat(configPath)
		if err != nil {
			if os.IsNotExist(err) {
				log.Printf("File %s not found, err: %v", configPath, err)
				continue
			}
			log.Printf("Error due checking config path %s, err: %v", configPath, err)
			continue
		}

		rawBytes, err := ioutil.ReadFile(configPath)
		if err != nil {
			return nil, err
		}
		configTemp := &ApplicationProbeConfig{}
		err = json.Unmarshal(rawBytes, configTemp)
		if err != nil {
			return nil, err
		}

		dbUri := os.Getenv(configTemp.DbUri)
		if dbUri == "" {
			return nil, fmt.Errorf(
				"unable to load database URI for service %s with probe %s", configTemp.Application, configTemp.Probe.Name,
			)
		}

		// Link worker function
		switch configTemp.Application {
		case "engine":
			engineWorker := engine.ENGINE_SUPPORTED_WORKERS[fmt.Sprintf("%s-%s", configTemp.Application, configTemp.Probe.Name)]
			if engineWorker.ExecFunction == nil {
				log.Printf("Function for application %s with probe %s not found, removed from the list", configTemp.Application, configTemp.Probe.Name)
				continue
			}
			configs = append(configs, ApplicationProbeConfig{
				Application: configTemp.Application,
				DbUri:       dbUri,
				DbTimeout:   configTemp.DbTimeout,
				Probe: probes.ApplicationProbe{
					Interval:     configTemp.Probe.Interval,
					ExecFunction: engineWorker.ExecFunction,
				},
			})
			log.Printf("[%s] [%s] - Registered function", configTemp.Application, configTemp.Probe.Name)
		default:
			log.Printf("Unsupported %s application with %s probe from the config", configTemp.Application, configTemp.Probe.Name)
		}
	}

	return &configs, nil
}
