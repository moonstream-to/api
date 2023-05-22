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

	humbug "github.com/bugout-dev/humbug/go/pkg"
)

var (
	accessIdCache AccessCache
)

type AccessCache struct {
	accessIds map[string]ClientAccess

	mux sync.RWMutex
}

// CreateAccessCache generates empty cache of client access
func CreateAccessCache() {
	accessIdCache = AccessCache{
		accessIds: make(map[string]ClientAccess),
	}
}

// Get access id from cache if exists
func (ac *AccessCache) FindAccessIdInCache(accessId string) string {
	var detectedId string

	ac.mux.RLock()
	for id := range ac.accessIds {
		if id == accessId {
			detectedId = id
			break
		}
	}
	ac.mux.RUnlock()

	return detectedId
}

// Update last call access timestamp and datasource for access id
func (ac *AccessCache) UpdateAccessIdAtCache(accessId, requestedDataSource string, tsNow int64) {
	ac.mux.Lock()
	if accessData, ok := ac.accessIds[accessId]; ok {
		accessData.LastAccessTs = tsNow
		accessData.requestedDataSource = requestedDataSource
		accessData.LastSessionCallsCounter++

		ac.accessIds[accessId] = accessData
	}
	ac.mux.Unlock()
}

// Add new access ID with data to cache
func (ac *AccessCache) AddAccessIdToCache(clientAccess ClientAccess, tsNow int64) {
	ac.mux.Lock()
	ac.accessIds[clientAccess.ClientResourceData.AccessID] = ClientAccess{
		ResourceID: clientAccess.ResourceID,

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
		},

		LastAccessTs:            tsNow,
		LastSessionAccessTs:     tsNow,
		LastSessionCallsCounter: 1,

		requestedDataSource: clientAccess.requestedDataSource,
	}
	ac.mux.Unlock()
}

// Check each access id in cache if it exceeds lifetime
func (ac *AccessCache) Cleanup() (int64, int64) {
	var removedAccessIds, totalAccessIds int64
	tsNow := time.Now().Unix()

	ac.mux.Lock()
	for aId, clientAccess := range ac.accessIds {
		if tsNow-clientAccess.LastAccessTs > NB_CACHE_ACCESS_ID_LIFETIME {
			// Remove clients who is not active for NB_CACHE_ACCESS_ID_LIFETIME lifetime period
			delete(ac.accessIds, aId)
			removedAccessIds++
			err := clientAccess.UpdateClientResourceCallCounter(tsNow)
			if err != nil {
				log.Printf("Unable to update Brood resource, err: %v\n", err)
			}
		} else if tsNow-clientAccess.LastSessionAccessTs > NB_CACHE_ACCESS_ID_SESSION_LIFETIME {
			// Remove clients with too long sessions, greater then NB_CACHE_ACCESS_ID_SESSION_LIFETIME
			delete(ac.accessIds, aId)
			removedAccessIds++
			err := clientAccess.UpdateClientResourceCallCounter(tsNow)
			if err != nil {
				log.Printf("Unable to update Brood resource, err: %v\n", err)
			}
		} else {
			totalAccessIds++
		}
	}
	ac.mux.Unlock()

	return removedAccessIds, totalAccessIds
}

func initCacheCleaning(debug bool) {
	t := time.NewTicker(NB_CACHE_CLEANING_INTERVAL)
	for {
		select {
		case <-t.C:
			removedAccessIds, totalAccessIds := accessIdCache.Cleanup()
			if debug {
				log.Printf("Removed %d clients from access cache", removedAccessIds)
			}
			log.Printf("Clients in access cache: %d", totalAccessIds)
		}
	}
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
	requestedDataSource := "database"

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

		if accessID == "" {
			http.Error(w, "No access id passed with request", http.StatusForbidden)
			return
		}

		tsNow := time.Now().Unix()

		// If access id does not belong to internal crawlers, then check cache or find it in Bugout resources
		if accessID == NB_CONTROLLER_ACCESS_ID {
			currentClientAccess = internalUsageAccess
			if stateCLI.enableDebugFlag {
				log.Printf("Access ID belongs to internal usage for user with ID %s", currentClientAccess.ClientResourceData.UserID)
			}
			currentClientAccess.LastAccessTs = tsNow
			currentClientAccess.requestedDataSource = requestedDataSource
		} else if accessIdCache.FindAccessIdInCache(accessID) != "" {
			currentClientAccess = accessIdCache.accessIds[accessID]
			if stateCLI.enableDebugFlag {
				log.Printf("Access ID found in cache for user with ID %s", currentClientAccess.ClientResourceData.UserID)
			}
			// Check if limit of calls not exceeded
			isClientAllowedToGetAccess := currentClientAccess.CheckClientCallPeriodLimits(tsNow)
			if !isClientAllowedToGetAccess {
				http.Error(w, "User exceeded limit of calls per period", http.StatusForbidden)
				return
			}
			currentClientAccess.requestedDataSource = requestedDataSource
			accessIdCache.UpdateAccessIdAtCache(accessID, requestedDataSource, tsNow)
		} else {
			if stateCLI.enableDebugFlag {
				log.Printf("New access id, looking at Brood resources")
			}
			resources, err := bugoutClient.Brood.GetResources(
				NB_CONTROLLER_TOKEN,
				NB_APPLICATION_ID,
				map[string]string{"access_id": accessID},
			)
			if err != nil {
				http.Error(w, "Unable to get user with provided access identifier", http.StatusForbidden)
				return
			}
			resourcesLen := len(resources.Resources)
			if resourcesLen == 0 {
				http.Error(w, "User with provided access identifier not found", http.StatusForbidden)
				return
			}
			if resourcesLen > 1 {
				http.Error(w, "User with provided access identifier has several access IDs", http.StatusInternalServerError)
				return
			}
			resourceData, err := json.Marshal(resources.Resources[0].ResourceData)
			if err != nil {
				http.Error(w, "Unable to encode resource data interface to json", http.StatusInternalServerError)
				return
			}
			currentClientAccess.ResourceID = resources.Resources[0].Id
			currentClientAccess.requestedDataSource = requestedDataSource
			err = json.Unmarshal(resourceData, &currentClientAccess.ClientResourceData)
			if err != nil {
				http.Error(w, "Unable to decode resource data json to structure", http.StatusInternalServerError)
				return
			}

			// Check if limit of calls not exceeded
			isClientAllowedToGetAccess := currentClientAccess.CheckClientCallPeriodLimits(tsNow)
			if !isClientAllowedToGetAccess {
				http.Error(w, "User exceeded limit of calls per period", http.StatusForbidden)
				return
			}
			accessIdCache.AddAccessIdToCache(currentClientAccess, tsNow)
		}

		ctxUser := context.WithValue(r.Context(), "currentClientAccess", currentClientAccess)

		next.ServeHTTP(w, r.WithContext(ctxUser))
	})
}
