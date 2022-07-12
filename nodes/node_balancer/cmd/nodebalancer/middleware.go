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
	accessIds map[string]ClientResourceData

	mux sync.RWMutex
}

func CreateAccessCache() {
	accessIdCache = AccessCache{
		accessIds: make(map[string]ClientResourceData),
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
func (ac *AccessCache) UpdateAccessIdAtCache(accessId, dataSource string) {
	ac.mux.Lock()
	if accessData, ok := ac.accessIds[accessId]; ok {
		accessData.LastAccessTs = time.Now().Unix()
		accessData.dataSource = dataSource

		ac.accessIds[accessId] = accessData
	}
	ac.mux.Unlock()
}

// Add new access id with data to cache
func (ac *AccessCache) AddAccessIdToCache(clientResourceData ClientResourceData, dataSource string) {
	ac.mux.Lock()
	ac.accessIds[clientResourceData.AccessID] = ClientResourceData{
		UserID:           clientResourceData.UserID,
		AccessID:         clientResourceData.AccessID,
		Name:             clientResourceData.Name,
		Description:      clientResourceData.Description,
		BlockchainAccess: clientResourceData.BlockchainAccess,
		ExtendedMethods:  clientResourceData.ExtendedMethods,

		LastAccessTs: time.Now().Unix(),

		dataSource: dataSource,
	}
	ac.mux.Unlock()
}

// Check each access id in cache if it exceeds lifetime
func (ac *AccessCache) Cleanup() (int64, int64) {
	var removedAccessIds, totalAccessIds int64
	tsNow := time.Now().Unix()
	ac.mux.Lock()
	for aId, aData := range ac.accessIds {
		if tsNow-aData.LastAccessTs > NB_CACHE_ACCESS_ID_LIFETIME {
			delete(ac.accessIds, aId)
			removedAccessIds++
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
				log.Printf("Removed %d elements from access id cache", removedAccessIds)
			}
			log.Printf("Elements in access id cache: %d", totalAccessIds)
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
func extractDataSource(r *http.Request) string {
	dataSource := "database"

	dataSources := r.Header[strings.Title(NB_DATA_SOURCE_HEADER)]
	for _, h := range dataSources {
		dataSource = h
	}

	queries := r.URL.Query()
	for k, v := range queries {
		if k == "data_source" {
			dataSource = v[0]
		}
	}

	return dataSource
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
			var jsonrpcRequest JSONRPCRequest
			err = json.Unmarshal(body, &jsonrpcRequest)
			if err != nil {
				log.Printf("Unable to parse body, err: %v", err)
			}
			logStr += fmt.Sprintf(" %s", jsonrpcRequest.Method)
		}

		if stateCLI.enableDebugFlag {
			if r.URL.RawQuery != "" {
				logStr += fmt.Sprintf(" %s", r.URL.RawQuery)
			}
			accessID := extractAccessID(r)
			if accessID != "" {
				dataSource := extractDataSource(r)
				logStr += fmt.Sprintf(" %s %s", dataSource, accessID)
			}
		}
		log.Printf("%s\n", logStr)
	})
}

// Check access id was provided correctly and save user access configuration to request context
func accessMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var currentClientAccess ClientResourceData

		accessID := extractAccessID(r)
		dataSource := extractDataSource(r)

		if accessID == "" {
			http.Error(w, "No access id passed with request", http.StatusForbidden)
			return
		}

		// If access id does not belong to internal crawlers, then check cache or find it in Bugout resources
		if accessID == NB_CONTROLLER_ACCESS_ID {
			if stateCLI.enableDebugFlag {
				log.Printf("Access id belongs to internal crawlers")
			}
			currentClientAccess = internalCrawlersAccess
			currentClientAccess.dataSource = dataSource
		} else if accessIdCache.FindAccessIdInCache(accessID) != "" {
			if stateCLI.enableDebugFlag {
				log.Printf("Access id found in cache")
			}
			currentClientAccess = accessIdCache.accessIds[accessID]
			currentClientAccess.dataSource = dataSource
			accessIdCache.UpdateAccessIdAtCache(accessID, dataSource)
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
			if len(resources.Resources) == 0 {
				http.Error(w, "User with provided access identifier not found", http.StatusForbidden)
				return
			}
			resource_data, err := json.Marshal(resources.Resources[0].ResourceData)
			if err != nil {
				http.Error(w, "Unable to encode resource data interface to json", http.StatusInternalServerError)
				return
			}
			var clientResourceData ClientResourceData
			err = json.Unmarshal(resource_data, &clientResourceData)
			if err != nil {
				http.Error(w, "Unable to decode resource data json to structure", http.StatusInternalServerError)
				return
			}
			currentClientAccess = ClientResourceData{
				UserID:           clientResourceData.UserID,
				AccessID:         clientResourceData.AccessID,
				Name:             clientResourceData.Name,
				Description:      clientResourceData.Description,
				BlockchainAccess: clientResourceData.BlockchainAccess,
				ExtendedMethods:  clientResourceData.ExtendedMethods,

				dataSource: dataSource,
			}

			accessIdCache.AddAccessIdToCache(clientResourceData, dataSource)
		}

		ctxUser := context.WithValue(r.Context(), "currentClientAccess", currentClientAccess)

		next.ServeHTTP(w, r.WithContext(ctxUser))
	})
}
