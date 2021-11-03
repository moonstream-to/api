package settings

import (
	"os"
)

// Geth configs
var MOONSTREAM_IPC_PATH = os.Getenv("MOONSTREAM_IPC_PATH")

// CORS
var MOONSTREAM_CORS_ALLOWED_ORIGINS = os.Getenv("MOONSTREAM_CORS_ALLOWED_ORIGINS")
