/*
Server API middlewares.
*/
package cmd

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

	"github.com/bugout-dev/moonstream/nodes/node_balancer/configs"

	humbug "github.com/bugout-dev/humbug/go/pkg"
)

// Extract access_id from header and query. Query takes precedence over header.
func extractAccessID(r *http.Request) string {
	var accessID string

	accessIDHeaders := r.Header[strings.Title(configs.NB_ACCESS_ID_HEADER)]
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

	dataSources := r.Header[strings.Title(configs.NB_DATA_SOURCE_HEADER)]
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

		ip, _, err := net.SplitHostPort(r.RemoteAddr)
		if err != nil {
			http.Error(w, fmt.Sprintf("Unable to parse client IP: %s", r.RemoteAddr), http.StatusBadRequest)
			return
		}
		logStr := fmt.Sprintf("%s %s %s", ip, r.Method, r.URL.Path)

		// Parse body and log method if jsonrpc path
		pathSlice := strings.Split(r.URL.Path, "/")
		if r.Method == "POST" && pathSlice[len(pathSlice)-1] == "jsonrpc" {
			var jsonrpcRequest JSONRPCRequest
			err = json.Unmarshal(body, &jsonrpcRequest)
			if err != nil {
				log.Printf("Unable to parse body %v", err)
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
		var currentUserAccess UserAccess

		accessID := extractAccessID(r)
		dataSource := extractDataSource(r)

		if accessID == "" {
			http.Error(w, "No access id passed with request", http.StatusForbidden)
			return
		}

		// If access id does not belong to internal crawlers, then find it in Bugout resources
		if accessID == configs.NB_CONTROLLER_ACCESS_ID {
			currentUserAccess = internalCrawlersAccess
			currentUserAccess.dataSource = dataSource
		} else {
			resources, err := bugoutClient.Brood.GetResources(
				configs.NB_CONTROLLER_TOKEN,
				configs.NB_APPLICATION_ID,
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
			var userAccess UserAccess
			err = json.Unmarshal(resource_data, &userAccess)
			if err != nil {
				http.Error(w, "Unable to decode resource data json to structure", http.StatusInternalServerError)
				return
			}
			currentUserAccess = UserAccess{
				UserID:           userAccess.UserID,
				AccessID:         userAccess.AccessID,
				Name:             userAccess.Name,
				Description:      userAccess.Description,
				BlockchainAccess: userAccess.BlockchainAccess,
				ExtendedMethods:  userAccess.ExtendedMethods,

				dataSource: dataSource,
			}
		}

		ctxUser := context.WithValue(r.Context(), "currentUserAccess", currentUserAccess)

		next.ServeHTTP(w, r.WithContext(ctxUser))
	})
}
