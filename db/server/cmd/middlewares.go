package cmd

import (
	"log"
	"net/http"
	"strings"
	"time"

	settings "github.com/bugout-dev/moonstream/db/server/configs"
)

// Handle panic errors to prevent server shutdown
func panicMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Println("recovered", err)
				http.Error(w, "Internal server error", 500)
			}
		}()
		// There will be a defer with panic handler in each next function
		next.ServeHTTP(w, r)
	})
}

// Log requests in proper format
func logsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("%s %s %s %s\n", time.Since(start), r.Method, r.URL.Path, r.RemoteAddr)
	})
}

// CORS middleware
func corsMiddleware(next http.Handler) http.Handler {
	// Iterate over list of allowed origins
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		for _, allowedOrigin := range strings.Split(settings.MOONSTREAM_CORS_ALLOWED_ORIGINS, ",") {
			if r.Header.Get("Origin") == allowedOrigin {
				w.Header().Set("Access-Control-Allow-Origin", allowedOrigin)
			}
		}
		if r.Method == "OPTIONS" {
			w.Header().Set("Access-Control-Allow-Methods", "GET,OPTIONS")
			// Credentials are cookies, authorization headers, or TLS client certificates
			w.Header().Set("Access-Control-Allow-Credentials", "true")
			w.Header().Set("Access-Control-Allow-Headers", "Authorization")
		}
		next.ServeHTTP(w, r)
	})
}
