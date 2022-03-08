/*
Server API middlewares.
*/
package cmd

import (
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

// Bugout authentication
func authMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeaders := r.Header["Authorization"]
		authHeadersLen := len(authHeaders)
		if authHeadersLen == 0 {
			http.Error(w, "Authorization header not found", http.StatusForbidden)
			return
		}
		if authHeadersLen > 1 {
			http.Error(w, "Too many authorization headers provided", http.StatusBadRequest)
			return
		}
		authHeader := authHeaders[0]

		// Extract Bearer token
		headerSlice := strings.Split(authHeader, " ")
		if len(headerSlice) != 2 {
			http.Error(w, "Unacceptable token format provided", http.StatusBadRequest)
			return
		}
		if headerSlice[0] != "Bearer" {
			http.Error(w, "Unacceptable token format provided", http.StatusBadRequest)
			return
		}

		// Check token is active
		client := http.Client{Timeout: configs.BUGOUT_AUTH_CALL_TIMEOUT}
		authReq, err := http.NewRequest("GET", fmt.Sprintf("%s/user", configs.BUGOUT_AUTH_URL), nil)
		if err != nil {
			http.Error(w, "Unable to construct authorization request", http.StatusInternalServerError)
			return
		}
		authReq.Header.Set("Authorization", authHeader)
		resp, err := client.Do(authReq)
		if err != nil {
			http.Error(w, "Unable to reach authorization server", http.StatusInternalServerError)
			return
		}
		defer resp.Body.Close()

		// Parse response from authorization server
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			http.Error(w, "Unable to read respose from authorization server", http.StatusInternalServerError)
			return
		}
		var userResponse BugoutUserResponse
		err = json.Unmarshal(body, &userResponse)
		if err != nil {
			http.Error(w, "Unable to parse respose from authorization server", http.StatusInternalServerError)
			return
		}
		if userResponse.ID == "" {
			http.Error(w, "Wrong authorization header", http.StatusForbidden)
			return
		}
		if userResponse.ApplicationID != configs.BUGOUT_NODE_BALANCER_APPLICATION_ID {
			http.Error(w, "Wrong authorization header", http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)
	})
}
