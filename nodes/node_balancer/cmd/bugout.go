package cmd

import (
	"bytes"
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
	var userResponse BugoutUserResponse

	url := fmt.Sprintf("%s/user", configs.BUGOUT_AUTH_URL)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return userResponse, err
	}

	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return userResponse, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return userResponse, err
	}
	err = json.Unmarshal(body, &userResponse)
	if err != nil {
		return userResponse, err
	}

	return userResponse, nil
}

// Find Bugout user
func (bc *BugoutClient) FindUser(token, userID string) (BugoutUserResponse, error) {
	var userResponse BugoutUserResponse

	url := fmt.Sprintf("%s/user/find?user_id=%s", configs.BUGOUT_AUTH_URL, userID)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return userResponse, err
	}

	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return userResponse, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return userResponse, err
	}
	err = json.Unmarshal(body, &userResponse)
	if err != nil {
		return userResponse, err
	}

	return userResponse, nil
}

func (bc *BugoutClient) AddUserAccess(token string, proposedUserAccess UserAccess) (UserAccess, error) {
	var userAccess UserAccess

	// Check user exists
	user, err := bc.FindUser(token, proposedUserAccess.UserID)
	if err != nil {
		return userAccess, err
	}
	if user == (BugoutUserResponse{}) {
		return userAccess, fmt.Errorf("User with id %s not found", proposedUserAccess.UserID)
	}

	resource := map[string]interface{}{
		"application_id": configs.NB_APPLICATION_ID,
		"resource_data":  proposedUserAccess,
	}
	resourceJson, err := json.Marshal(resource)
	if err != nil {
		return userAccess, err
	}
	url := fmt.Sprintf("%s/resources", configs.BUGOUT_AUTH_URL)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(resourceJson))
	if err != nil {
		return userAccess, err
	}
	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
		"Content-Type":  []string{"application/json"},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return userAccess, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return userAccess, err
	}
	var resourceResponse BugoutResourceResponse
	err = json.Unmarshal(body, &resourceResponse)
	if err != nil {
		return userAccess, err
	}

	userAccess = resourceResponse.ResourceData

	return userAccess, nil
}

// Get Bugout resource
func (bc *BugoutClient) GetResources(token, userID, accessID string) (BugoutResourcesResponse, error) {
	var resourcesResponse BugoutResourcesResponse

	url := fmt.Sprintf("%s/resources?application_id=%s", configs.BUGOUT_AUTH_URL, configs.NB_APPLICATION_ID)
	if userID != "" {
		url += fmt.Sprintf("&user_id=%s", userID)
	}
	if accessID != "" {
		url += fmt.Sprintf("&access_id=%s", accessID)
	}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return resourcesResponse, err
	}
	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return resourcesResponse, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return resourcesResponse, err
	}
	err = json.Unmarshal(body, &resourcesResponse)
	if err != nil {
		return resourcesResponse, err
	}

	return resourcesResponse, nil
}

func (bc *BugoutClient) DeleteResource(token, resourceID string) (BugoutResourceResponse, error) {
	var resourceResponse BugoutResourceResponse

	url := fmt.Sprintf("%s/resources/%s", configs.BUGOUT_AUTH_URL, resourceID)
	req, err := http.NewRequest("DELETE", url, nil)
	if err != nil {
		return resourceResponse, err
	}
	req.Header = http.Header{
		"Authorization": []string{fmt.Sprintf("Bearer %s", token)},
	}
	resp, err := bc.Client.Do(req)
	if err != nil {
		return resourceResponse, err
	}
	defer resp.Body.Close()

	// Parse response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return resourceResponse, err
	}
	err = json.Unmarshal(body, &resourceResponse)
	if err != nil {
		return resourceResponse, err
	}

	return resourceResponse, nil
}
