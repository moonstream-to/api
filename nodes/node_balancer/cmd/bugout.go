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

// Get Bugout resources
func (bc *BugoutClient) GetResources(token string, userID string) (BugoutResourcesResponse, error) {
	url := fmt.Sprintf("%s/resources?application_id=%s", configs.BUGOUT_AUTH_URL, configs.BUGOUT_NODE_BALANCER_APPLICATION_ID)
	if userID != "" {
		url += fmt.Sprintf("&user_id=%s", userID)
	}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return BugoutResourcesResponse{}, err
	}
	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return BugoutResourcesResponse{}, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return BugoutResourcesResponse{}, err
	}
	var resourcesResponse BugoutResourcesResponse
	err = json.Unmarshal(body, &resourcesResponse)
	if err != nil {
		return BugoutResourcesResponse{}, err
	}

	return resourcesResponse, nil
}
