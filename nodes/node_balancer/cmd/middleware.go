/*
Server API middlewares.
*/
package cmd

import (
	"log"
	"net"
	"net/http"

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
