/*
Server API middleware.
*/
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/bugout-dev/bugout-go/pkg/brood"
	humbug "github.com/bugout-dev/humbug/go/pkg"
	"github.com/google/uuid"
)

var (
	accessCache AccessCache
)

// AccessCache caches client identification for fast access to nodes
//
// If authorization passed with Bearer token, then it triggers to fetch Brood resource with access ID
// or create new one. After it under key `accessIds` and `authorizationTokens` will be added similar
// address pointers to one `ClientAccess`.
type AccessCache struct {
	accessIds           map[string]*ClientAccess
	authorizationTokens map[string]*ClientAccess

	mux sync.RWMutex
}

// CreateAccessCache generates empty cache of client access
func CreateAccessCache() {
	accessCache = AccessCache{
		accessIds:           make(map[string]*ClientAccess),
		authorizationTokens: make(map[string]*ClientAccess),
	}
}

// FindAccessIdInCache looking for user access in `accessIds` cache
func (ac *AccessCache) isAccessIdInCache(accessId string) bool {
	detected := false

	ac.mux.RLock()
	for id := range ac.accessIds {
		if id == accessId {
			detected = true
			break
		}
	}
	ac.mux.RUnlock()

	return detected
}

// FindAuthorizationTokenInCache looking for user access in `authorizationTokens` cache
func (ac *AccessCache) isAuthorizationTokenInCache(authorizationToken string) bool {
	detected := false

	ac.mux.RLock()
	for id := range ac.authorizationTokens {
		if id == authorizationToken {
			detected = true
			break
		}
	}
	ac.mux.RUnlock()

	return detected
}

// Update last call access timestamp and datasource for user access
func (ac *AccessCache) UpdateAccessAtCache(accessId, authorizationToken, requestedDataSource string, tsNow int64) {
	ac.mux.Lock()
	var accessToModify *ClientAccess

	if accessId != "" {
		if access, ok := ac.accessIds[accessId]; ok {
			accessToModify = access

		}
	}

	if authorizationToken != "" {
		if access, ok := ac.authorizationTokens[authorizationToken]; ok {
			accessToModify = access
		}
	}

	accessToModify.LastAccessTs = tsNow
	accessToModify.requestedDataSource = requestedDataSource
	accessToModify.LastSessionCallsCounter++

	ac.mux.Unlock()
}

// Add new user access identifier with data to cache
func (ac *AccessCache) AddAccessToCache(clientAccess ClientAccess, tsNow int64) error {
	_, err := uuid.Parse(clientAccess.ClientResourceData.AccessID)
	if err != nil {
		log.Printf("Access ID %s is not valid UUID, err: %v", clientAccess.ClientResourceData.AccessID, err)
		return fmt.Errorf("access ID is not valid UUID")
	}

	ac.mux.Lock()
	access := &ClientAccess{
		ResourceID:         clientAccess.ResourceID,
		authorizationToken: clientAccess.authorizationToken,

		ClientResourceData: ClientResourceData{
			UserID:           clientAccess.ClientResourceData.UserID,
			AccessID:         clientAccess.ClientResourceData.AccessID,
			Name:             clientAccess.ClientResourceData.Name,
			Description:      clientAccess.ClientResourceData.Description,
			BlockchainAccess: clientAccess.ClientResourceData.BlockchainAccess,
			ExtendedMethods:  clientAccess.ClientResourceData.ExtendedMethods,

			PeriodDuration:    clientAccess.ClientResourceData.PeriodDuration,
			PeriodStartTs:     clientAccess.ClientResourceData.PeriodStartTs,
			MaxCallsPerPeriod: clientAccess.ClientResourceData.MaxCallsPerPeriod,
			CallsPerPeriod:    clientAccess.ClientResourceData.CallsPerPeriod,

			Type: clientAccess.ClientResourceData.Type,
		},

		LastAccessTs:            tsNow,
		LastSessionAccessTs:     tsNow,
		LastSessionCallsCounter: 1,

		requestedDataSource: clientAccess.requestedDataSource,
	}

	ac.accessIds[clientAccess.ClientResourceData.AccessID] = access
	if clientAccess.authorizationToken != "" {
		ac.authorizationTokens[clientAccess.authorizationToken] = access
	}
	ac.mux.Unlock()

	return nil
}

// Check each access id in cache if it exceeds lifetime
func (ac *AccessCache) Cleanup() (int64, int64) {
	var removedAccessIds, totalAccessIds int64
	tsNow := time.Now().Unix()

	ac.mux.Lock()

	for aId, clientAccess := range ac.accessIds {
		totalAccessIds++
		removedUserId := ""

		if tsNow-clientAccess.LastAccessTs > NB_CACHE_ACCESS_ID_LIFETIME {
			// Remove clients who is not active for NB_CACHE_ACCESS_ID_LIFETIME lifetime period
			removedUserId = clientAccess.ClientResourceData.UserID
			delete(ac.accessIds, aId)
			removedAccessIds++
			err := clientAccess.UpdateClientResourceCallCounter(tsNow)
			if err != nil {
				log.Printf("Unable to update Brood resource, err: %v\n", err)
			}
		} else if tsNow-clientAccess.LastSessionAccessTs > NB_CACHE_ACCESS_ID_SESSION_LIFETIME {
			removedUserId = clientAccess.ClientResourceData.UserID
			// Remove clients with too long sessions, greater then NB_CACHE_ACCESS_ID_SESSION_LIFETIME
			delete(ac.accessIds, aId)
			removedAccessIds++
			err := clientAccess.UpdateClientResourceCallCounter(tsNow)
			if err != nil {
				log.Printf("Unable to update Brood resource, err: %v\n", err)
			}
		}

		if removedUserId != "" {
			for aToken, clientAccess := range ac.authorizationTokens {
				if clientAccess.ClientResourceData.UserID == removedUserId {
					delete(ac.authorizationTokens, aToken)
				}
			}
			removedUserId = ""
		}
	}
	ac.mux.Unlock()

	totalAccessIds = totalAccessIds - removedAccessIds

	return removedAccessIds, totalAccessIds
}

func initCacheCleaning(debug bool) {
	t := time.NewTicker(NB_CACHE_CLEANING_INTERVAL)
	for {
		select {
		case <-t.C:
			removedAccessIds, totalAccessIds := accessCache.Cleanup()
			if debug {
				log.Printf("Removed %d clients from access cache", removedAccessIds)
			}
			log.Printf("Clients in access cache: %d", totalAccessIds)
		}
	}
}

// fetchClientAccessFromResources get resources with access ID or authorization token and generate new one if there no one
func fetchClientAccessFromResources(accessID, authorizationToken string, tsNow int64) (*ClientAccess, error) {
	var err error

	queryParameters := map[string]string{"type": BUGOUT_RESOURCE_TYPE_NODEBALANCER_ACCESS}
	if accessID != "" {
		queryParameters["access_id"] = accessID
	}

	token := NB_CONTROLLER_TOKEN
	if authorizationToken != "" {
		token = authorizationToken
	}

	var resources brood.Resources
	resources, err = bugoutClient.Brood.GetResources(
		token,
		MOONSTREAM_APPLICATION_ID,
		queryParameters,
	)
	if err != nil {
		log.Printf("Unable to get resources, err: %v", err)
		return nil, fmt.Errorf("unable to get access identifiers")
	}

	if len(resources.Resources) == 0 {
		if authorizationToken != "" {
			// Generate new autogenerated access resource with default parameters and grant user permissions to work with it
			user, err := bugoutClient.Brood.GetUser(authorizationToken)
			if err != nil {
				log.Printf("Unable to get user, err: %v", err)
				return nil, fmt.Errorf("unable to find user with provided authorization token")
			}
			newResource, err := bugoutClient.Brood.CreateResource(
				NB_CONTROLLER_TOKEN, MOONSTREAM_APPLICATION_ID, ClientResourceData{
					UserID:           user.Id,
					AccessID:         uuid.New().String(),
					Name:             user.Username,
					Description:      "Autogenerated access ID",
					BlockchainAccess: true,
					ExtendedMethods:  false,

					PeriodDuration:    DEFAULT_AUTOGENERATED_PERIOD_DURATION,
					PeriodStartTs:     tsNow,
					MaxCallsPerPeriod: DEFAULT_AUTOGENERATED_MAX_CALLS_PER_PERIOD,
					CallsPerPeriod:    0,

					Type: BUGOUT_RESOURCE_TYPE_NODEBALANCER_ACCESS,
				},
			)
			if err != nil {
				log.Printf("Unable to create resource with autogenerated access for user with ID %s, err: %v", user.Id, err)
				return nil, fmt.Errorf("unable to create resource with autogenerated access for user")
			}

			resourceHolderPermissions, err := bugoutClient.Brood.AddResourceHolderPermissions(
				NB_CONTROLLER_TOKEN, newResource.Id, brood.ResourceHolder{
					Id:          user.Id,
					HolderType:  "user",
					Permissions: DEFAULT_AUTOGENERATED_USER_PERMISSIONS,
				},
			)
			if err != nil {
				log.Printf("Unable to grant permissions to user with ID %s at resource with ID %s, err: %v", newResource.Id, user.Id, err)
				return nil, fmt.Errorf("unable to create resource with autogenerated access for user")
			}

			log.Printf("Created new resource with ID %s with autogenerated access for user with ID %s", resourceHolderPermissions.ResourceId, user.Id)
			resources.Resources = append(resources.Resources, newResource)
		} else {
			return nil, fmt.Errorf("there are no provided access identifier")
		}
	} else if len(resources.Resources) > 1 {
		// TODO(kompotkot): Write support of multiple resources, be careful, because NB_CONTROLLER has several resources
		return nil, fmt.Errorf("there are no provided access identifier")
	}

	var clientAccessRaw ClientAccess
	resourceData, err := json.Marshal(&resources.Resources[0].ResourceData)
	if err != nil {
		log.Printf("Unable to parse resource data to access identifier, err: %v", err)
		return nil, fmt.Errorf("unable to parse resource data to access identifier")
	}
	err = json.Unmarshal(resourceData, &clientAccessRaw.ClientResourceData)
	if err != nil {
		log.Printf("Unable to decode resource data to access identifier, err: %v", err)
		return nil, fmt.Errorf("unable to decode resource data to access identifier")
	}
	clientAccessRaw.ResourceID = resources.Resources[0].Id

	return &clientAccessRaw, nil
}

// Extract access_id from header and query. Query takes precedence over header.
func extractAccessID(r *http.Request) string {
	var accessID string

	accessIDHeaders := r.Header[strings.Title(NB_ACCESS_ID_HEADER)]
	for _, h := range accessIDHeaders {
		accessID = h
	}

	queries := r.URL.Query()
	for k, v := range queries {
		if k == "access_id" {
			accessID = v[0]
		}
	}

	return accessID
}

// Extract data_source from header and query. Query takes precedence over header.
func extractRequestedDataSource(r *http.Request) string {
	requestedDataSource := "blockchain"

	requestedDataSources := r.Header[strings.Title(NB_DATA_SOURCE_HEADER)]
	for _, h := range requestedDataSources {
		requestedDataSource = h
	}

	queries := r.URL.Query()
	for k, v := range queries {
		if k == "data_source" {
			requestedDataSource = v[0]
		}
	}

	return requestedDataSource
}

// Handle panic errors to prevent server shutdown
func panicMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Println("recovered", err)
				report := humbug.PanicReport(err)
				reporter.Publish(report)
				http.Error(w, "Internal server error", 500)
			}
		}()

		// There will be a defer with panic handler in each next function
		next.ServeHTTP(w, r)
	})
}

// CORS middleware
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodOptions {
			for _, allowedOrigin := range strings.Split(MOONSTREAM_CORS_ALLOWED_ORIGINS, ",") {
				if r.Header.Get("Origin") == allowedOrigin {
					w.Header().Set("Access-Control-Allow-Origin", allowedOrigin)
					w.Header().Set("Access-Control-Allow-Methods", "GET,POST")
					// Credentials are cookies, authorization headers, or TLS client certificates
					w.Header().Set("Access-Control-Allow-Credentials", "true")
					w.Header().Set("Access-Control-Allow-Headers", "Authorization, Content-Type")
				}
			}
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

// Split JSON RPC request to object and slice and return slice of requests
func jsonrpcRequestParser(body []byte) ([]JSONRPCRequest, error) {
	var jsonrpcRequest []JSONRPCRequest

	firstByte := bytes.TrimLeft(body, " \t\r\n")
	switch {
	case len(firstByte) > 0 && firstByte[0] == '[':
		err := json.Unmarshal(body, &jsonrpcRequest)
		if err != nil {
			return nil, fmt.Errorf("unable to parse body, err: %v", err)
		}
	case len(firstByte) > 0 && firstByte[0] == '{':
		var singleJsonrpcRequest JSONRPCRequest
		err := json.Unmarshal(body, &singleJsonrpcRequest)
		if err != nil {
			return nil, fmt.Errorf("unable to parse body, err: %v", err)
		}
		jsonrpcRequest = []JSONRPCRequest{singleJsonrpcRequest}
	default:
		return nil, fmt.Errorf("incorrect first byte in JSON RPC request")
	}

	return jsonrpcRequest, nil
}

// Log access requests in proper format
func logMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, "Unable to read body", http.StatusBadRequest)
			return
		}
		r.Body = ioutil.NopCloser(bytes.NewBuffer(body))
		if len(body) > 0 {
			defer r.Body.Close()
		}

		next.ServeHTTP(w, r)

		var ip string
		realIp := r.Header["X-Real-Ip"]
		if len(realIp) == 0 {
			ip, _, err = net.SplitHostPort(r.RemoteAddr)
			if err != nil {
				http.Error(w, fmt.Sprintf("Unable to parse client IP: %s", r.RemoteAddr), http.StatusBadRequest)
				return
			}
		} else {
			ip = realIp[0]
		}
		logStr := fmt.Sprintf("%s %s %s", ip, r.Method, r.URL.Path)

		// Parse body and log method if jsonrpc path
		pathSlice := strings.Split(r.URL.Path, "/")
		if r.Method == "POST" && pathSlice[len(pathSlice)-1] == "jsonrpc" {
			jsonrpcRequests, err := jsonrpcRequestParser(body)
			if err != nil {
				log.Println(err)
			}
			for i, jsonrpcRequest := range jsonrpcRequests {
				if i == 0 {
					logStr += fmt.Sprintf(" [%s", jsonrpcRequest.Method)
				} else {
					logStr += fmt.Sprintf(" %s", jsonrpcRequest.Method)
				}
				if i == len(jsonrpcRequests)-1 {
					logStr += "]"
				}
			}
		}

		if stateCLI.enableDebugFlag {
			if r.URL.RawQuery != "" {
				logStr += fmt.Sprintf(" %s", r.URL.RawQuery)
			}
			accessID := extractAccessID(r)
			if accessID != "" {
				dataSource := extractRequestedDataSource(r)
				logStr += fmt.Sprintf(" %s %s", dataSource, accessID)
			}
		}
		log.Printf("%s\n", logStr)
	})
}

// Check access id was provided correctly and save user access configuration to request context
func accessMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var currentClientAccess ClientAccess

		accessID := extractAccessID(r)
		requestedDataSource := extractRequestedDataSource(r)

		// Extract Authorization token if Bearer header provided
		var authorizationTokenRaw string
		authorizationTokenHeaders := r.Header[strings.Title("authorization")]
		for _, h := range authorizationTokenHeaders {
			authorizationTokenRaw = h
		}
		var authorizationToken string
		if authorizationTokenRaw != "" {
			authorizationTokenSlice := strings.Split(authorizationTokenRaw, " ")
			if len(authorizationTokenSlice) != 2 || authorizationTokenSlice[0] != "Bearer" || authorizationTokenSlice[1] == "" {
				http.Error(w, "Wrong authorization token provided", http.StatusForbidden)
				return
			}
			authorizationToken = authorizationTokenSlice[1]
		}

		if accessID == "" && authorizationToken == "" {
			http.Error(w, "No access ID or authorization header passed with request", http.StatusForbidden)
			return
		}

		tsNow := time.Now().Unix()

		// If access id does not belong to internal crawlers, then check cache or find it in Bugout resources
		if accessID != "" && accessID == NB_CONTROLLER_ACCESS_ID {
			if stateCLI.enableDebugFlag {
				log.Printf("Access ID belongs to internal usage for user with ID %s", currentClientAccess.ClientResourceData.UserID)
			}
			currentClientAccess = internalUsageAccess
			currentClientAccess.LastAccessTs = tsNow
			currentClientAccess.requestedDataSource = requestedDataSource
		} else if accessID != "" && accessCache.isAccessIdInCache(accessID) {
			if stateCLI.enableDebugFlag {
				log.Printf("Access ID found in cache for user with ID %s", currentClientAccess.ClientResourceData.UserID)
			}
			currentClientAccess = *accessCache.accessIds[accessID]
			isClientAllowedToGetAccess := currentClientAccess.CheckClientCallPeriodLimits(tsNow)
			if !isClientAllowedToGetAccess {
				http.Error(w, "User exceeded limit of calls per period", http.StatusForbidden)
				return
			}
			currentClientAccess.requestedDataSource = requestedDataSource
			accessCache.UpdateAccessAtCache(accessID, authorizationToken, requestedDataSource, tsNow)
		} else if accessID == "" && accessCache.isAuthorizationTokenInCache(authorizationToken) {
			if stateCLI.enableDebugFlag {
				log.Printf("Client connected with Authorization token")
			}
			currentClientAccess = *accessCache.authorizationTokens[authorizationToken]
			isClientAllowedToGetAccess := currentClientAccess.CheckClientCallPeriodLimits(tsNow)
			if !isClientAllowedToGetAccess {
				http.Error(w, "User exceeded limit of calls per period", http.StatusForbidden)
				return
			}
			currentClientAccess.requestedDataSource = requestedDataSource
			accessCache.UpdateAccessAtCache(accessID, authorizationToken, requestedDataSource, tsNow)
		} else {
			if stateCLI.enableDebugFlag {
				log.Printf("No access identity found in cache, looking at Brood resources")
			}

			clientAccessRaw, err := fetchClientAccessFromResources(accessID, authorizationToken, tsNow)
			if err != nil {
				http.Error(w, fmt.Sprintf("%v", err), http.StatusForbidden)
				return
			}

			isClientAllowedToGetAccess := clientAccessRaw.CheckClientCallPeriodLimits(tsNow)
			if !isClientAllowedToGetAccess {
				http.Error(w, "User exceeded limit of calls per period", http.StatusForbidden)
				return
			}
			currentClientAccess = ClientAccess(*clientAccessRaw)
			currentClientAccess.authorizationToken = authorizationToken
			currentClientAccess.requestedDataSource = requestedDataSource

			// If client logged in before with access ID and it exists in cache, then re-use it
			// else create new instances in cache
			if authorizationToken != "" && accessCache.isAccessIdInCache(currentClientAccess.ClientResourceData.AccessID) {
				accessCache.authorizationTokens[authorizationToken] = accessCache.accessIds[currentClientAccess.ClientResourceData.AccessID]
			} else {
				if stateCLI.enableDebugFlag {
					log.Printf("Adding new access identifier in cache")
				}
				err := accessCache.AddAccessToCache(currentClientAccess, tsNow)
				if err != nil {
					http.Error(w, "Unable to add access ID to cache", http.StatusForbidden)
					return
				}
			}
		}

		ctxUser := context.WithValue(r.Context(), "currentClientAccess", currentClientAccess)

		next.ServeHTTP(w, r.WithContext(ctxUser))
	})
}
