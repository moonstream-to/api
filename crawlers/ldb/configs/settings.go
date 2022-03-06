package configs

import (
	"os"
	"time"
)

// Database configs
var MOONSTREAM_DB_MAX_IDLE_CONNS int = 30
var MOONSTREAM_DB_CONN_MAX_LIFETIME = 30 * time.Minute
var MOONSTREAM_DB_URI = os.Getenv("MOONSTREAM_DB_URI")

// Humber configs
var HUMBUG_LDB_CLIENT_ID = os.Getenv("HUMBUG_LDB_CLIENT_ID")
var HUMBUG_LDB_TOKEN = os.Getenv("HUMBUG_LDB_TOKEN")
