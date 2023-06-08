package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

type EntityInstance struct {
	PublicEndpoint string
	CollectionId   string
	CollectionName string

	Headers map[string]string
}

type EntityResponse struct {
	EntityId       string              `json:"entity_id"`
	CollectionId   string              `json:"collection_id"`
	Address        string              `json:"address"`
	Blockchain     string              `json:"blockchain"`
	Name           string              `json:"name"`
	RequiredFields []map[string]string `json:"required_fields"`
	CreatedAt      string              `json:"created_at"`
	UpdatedAt      string              `json:"updated_at"`
}

type EntitySearchResponse struct {
	TotalResults int64            `json:"total_results"`
	Offset       int64            `json:"offset"`
	NextOffset   int64            `json:"next_offset"`
	MaxScore     float64          `json:"max_score"`
	Entities     []EntityResponse `json:"entities"`
}

type EntityCollectionResponse struct {
	CollectionId string `json:"collection_id"`
	Name         string `json:"name"`
}

func InitializeEntityInstance(collectionId string) (*EntityInstance, error) {
	MOONSTREAM_ENTITY_URL := os.Getenv("MOONSTREAM_ENTITY_URL")
	if MOONSTREAM_ENTITY_URL == "" {
		return nil, errors.New("Environment variable MOONSTREAM_ENTITY_URL should be specified")
	}

	publicEndpoint := fmt.Sprintf("%s/public", MOONSTREAM_ENTITY_URL)
	headers := make(map[string]string)
	headers["X-Moonstream-Robots"] = "airdrop-robot"

	url := fmt.Sprintf("%s/collections/%s", publicEndpoint, collectionId)
	body, _, err := caller("GET", url, nil, headers, 15)
	if err != nil {
		return nil, err
	}

	var resp EntityCollectionResponse
	err = json.Unmarshal(*body, &resp)
	if err != nil {
		return nil, err
	}

	entityInstance := EntityInstance{
		PublicEndpoint: publicEndpoint,
		CollectionId:   collectionId,
		CollectionName: resp.Name,
		Headers:        headers,
	}

	return &entityInstance, nil
}

// Make HTTP calls to required servers
func caller(method, url string, reqBody io.Reader, headers map[string]string, timeout int) (*[]byte, int, error) {
	req, err := http.NewRequest(method, url, reqBody)
	if err != nil {
		return nil, 0, err
	}
	if len(headers) > 0 {
		for k, v := range headers {
			req.Header.Set(k, v)
		}
	}

	client := http.Client{Timeout: time.Second * time.Duration(timeout)}
	resp, err := client.Do(req)
	if err != nil {
		return nil, 0, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, resp.StatusCode, err
	}

	return &body, resp.StatusCode, nil
}

// FetchPublicSearchUntouched request not touched entities, ready to airdrop
// TODO(kompotkot): Pass with robots header unique identifier of robot
func (ec *EntityInstance) FetchPublicSearchUntouched(limit int) (int, EntitySearchResponse, error) {
	data := EntitySearchResponse{}

	url := fmt.Sprintf("%s/collections/%s/search?required_field=!touch:true&limit=%d", ec.PublicEndpoint, ec.CollectionId, limit)
	body, status_code, err := caller("GET", url, nil, ec.Headers, 15)
	if err != nil {
		return status_code, data, err
	}

	var resp EntitySearchResponse
	err = json.Unmarshal(*body, &resp)
	if err != nil {
		return status_code, data, err
	}
	data = resp

	return status_code, data, nil
}

// TODO(kompotkot): Create batch endpoint for tags creation
func (ec *EntityInstance) TouchPublicEntity(entityId string, timeout int) (int, []string, error) {
	var data []string

	url := fmt.Sprintf("%s/collections/%s/entities/%s", ec.PublicEndpoint, ec.CollectionId, entityId)
	body, status_code, err := caller("PUT", url, nil, ec.Headers, timeout)
	if err != nil {
		return status_code, data, err
	}

	var resp []string
	err = json.Unmarshal(*body, &resp)
	if err != nil {
		return status_code, data, err
	}
	data = resp

	return status_code, data, nil
}
