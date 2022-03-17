/*
Server API middlewares.
*/
package cmd

import (
	"context"
	"log"
	"net"
	"net/http"

	"github.com/bugout-dev/moonstream/nodes/node_balancer/configs"

	humbug "github.com/bugout-dev/humbug/go/pkg"
)

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
		next.ServeHTTP(w, r)
		ip, _, err := net.SplitHostPort(r.RemoteAddr)
		if err != nil {
			log.Printf("Unable to parse client IP: %s\n", r.RemoteAddr)
		} else {
			log.Printf("%s %s %s\n", ip, r.Method, r.URL.Path)
		}
	})
}

// Check access id was provided correctly and save user access configuration to request context
func accessMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var currentUserAccess UserAccess

		var accessID string
		accessIDHeaders := r.Header[configs.NB_ACCESS_ID_HEADER]
		for _, h := range accessIDHeaders {
			accessID = h
		}

		dataSource := "database"
		dataSources := r.Header[configs.NB_DATA_SOURCE_HEADER]
		for _, h := range dataSources {
			dataSource = h
		}

		queries := r.URL.Query()
		for k, v := range queries {
			if k == "access_id" {
				accessID = v[0]
			}
			if k == "data_source" {
				dataSource = v[0]
			}
		}

		if accessID == "" {
			http.Error(w, "No authorization header passed with request", http.StatusForbidden)
			return
		}

		// If access id does not belong to controller, then find it in Bugout resources
		if accessID == configs.NB_CONTROLLER_ACCESS_ID {
			currentUserAccess = controllerUserAccess
			currentUserAccess.dataSource = dataSource
		} else {
			resources, err := bugoutClient.GetResources(configs.NB_CONTROLLER_TOKEN, "", accessID)
			if err != nil {
				http.Error(w, "Unable to get user with provided access identifier", http.StatusForbidden)
				return
			}
			if len(resources.Resources) == 0 {
				http.Error(w, "User with provided access identifier not found", http.StatusForbidden)
				return
			}
			userAccess := resources.Resources[0].ResourceData
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
