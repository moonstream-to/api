/*
Configurations for load balancer server.
*/
package configs

import (
	"log"
	"os"
	"time"
)

var (
	// Bugout and application configuration
	BUGOUT_AUTH_URL          = os.Getenv("BUGOUT_AUTH_URL")
	BUGOUT_AUTH_CALL_TIMEOUT = time.Second * 5
	NB_APPLICATION_ID        = os.Getenv("NB_APPLICATION_ID")
	NB_CONTROLLER_TOKEN      = os.Getenv("NB_CONTROLLER_TOKEN")
	NB_CONTROLLER_ACCESS_ID  = os.Getenv("NB_CONTROLLER_ACCESS_ID")

	NB_CONNECTION_RETRIES          = 2
	NB_CONNECTION_RETRIES_INTERVAL = time.Millisecond * 10
	NB_HEALTH_CHECK_INTERVAL       = time.Second * 5
	NB_HEALTH_CHECK_CALL_TIMEOUT   = time.Second * 2

	// Client configuration
	NB_CLIENT_NODE_KEEP_ALIVE = int64(5) // How long to store node in hot list for client in seconds

	NB_ACCESS_ID_HEADER   = os.Getenv("NB_ACCESS_ID_HEADER")
	NB_DATA_SOURCE_HEADER = os.Getenv("NB_DATA_SOURCE_HEADER")

	// Humbug configuration
	HUMBUG_REPORTER_NB_TOKEN = os.Getenv("HUMBUG_REPORTER_NB_TOKEN")

	// Database configuration
	MOONSTREAM_DB_URI_READ_ONLY         = os.Getenv("MOONSTREAM_DB_URI_READ_ONLY")
	MOONSTREAM_DB_MAX_IDLE_CONNS    int = 30
	MOONSTREAM_DB_CONN_MAX_LIFETIME     = 30 * time.Minute
)

var MOONSTREAM_NODES_SERVER_PORT = os.Getenv("MOONSTREAM_NODES_SERVER_PORT")
var MOONSTREAM_CLIENT_ID_HEADER = os.Getenv("MOONSTREAM_CLIENT_ID_HEADER")

func CheckEnvVarSet() {
	if MOONSTREAM_CLIENT_ID_HEADER == "" {
		MOONSTREAM_CLIENT_ID_HEADER = "x-moonstream-client-id"
	}

	if MOONSTREAM_NODES_SERVER_PORT == "" {
		log.Fatal("Environment variable MOONSTREAM_NODES_SERVER_PORT not set")
	}
}
