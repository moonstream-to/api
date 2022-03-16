package cmd

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	configs "github.com/bugout-dev/moonstream/nodes/node_balancer/configs"
)

var (
	bugoutClient BugoutClient
)

type BugoutClient struct {
	Client  http.Client
	AuthURL string
}

type PingResponse struct {
	Status string `json:"status"`
}

// Bugout responses
type BugoutUserResponse struct {
	ID            string `json:"user_id"`
	ApplicationID string `json:"application_id"`
}

type UserAccess struct {
	UserID           string `json:"user_id"`
	AccessID         string `json:"access_id"`
	Name             string `json:"name"`
	Description      string `json:"description"`
	BlockchainAccess bool   `json:"blockchain_access"`
	ExtendedMethods  bool   `json:"extended_methods"`

	dataSource string
}

type BugoutResourceResponse struct {
	ID           string     `json:"id"`
	ResourceData UserAccess `json:"resource_data"`
}

type BugoutResourcesResponse struct {
	Resources []BugoutResourceResponse `json:"resources"`
}

// Initialize Bugout http client
func InitBugoutClient() {
	client := http.Client{Timeout: configs.BUGOUT_AUTH_CALL_TIMEOUT}
	bugoutClient = BugoutClient{
		Client:  client,
		AuthURL: configs.BUGOUT_AUTH_URL,
	}
}

// Get Bugout user
func (bc *BugoutClient) GetUser(token string) (BugoutUserResponse, error) {
	url := fmt.Sprintf("%s/user", configs.BUGOUT_AUTH_URL)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return BugoutUserResponse{}, err
	}

	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return BugoutUserResponse{}, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return BugoutUserResponse{}, err
	}
	var userResponse BugoutUserResponse
	err = json.Unmarshal(body, &userResponse)
	if err != nil {
		return BugoutUserResponse{}, err
	}

	return userResponse, nil
}

// Get user accesses from Bugout resources
func (bc *BugoutClient) GetUserAccesses(token, userID, accessID string) ([]UserAccess, error) {
	var userAccesses []UserAccess

	url := fmt.Sprintf("%s/resources?application_id=%s", configs.BUGOUT_AUTH_URL, configs.NB_APPLICATION_ID)
	if userID != "" {
		url += fmt.Sprintf("&user_id=%s", userID)
	}
	if accessID != "" {
		url += fmt.Sprintf("&access_id=%s", accessID)
	}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return userAccesses, err
	}
	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return userAccesses, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return userAccesses, err
	}
	var resourcesResponse BugoutResourcesResponse
	err = json.Unmarshal(body, &resourcesResponse)
	if err != nil {
		return userAccesses, err
	}

	for _, resourceData := range resourcesResponse.Resources {
		userAccesses = append(userAccesses, resourceData.ResourceData)
	}

	return userAccesses, nil
}
