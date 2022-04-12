package settings

import (
	"os"
)

var LOCAL_IPV4 = os.Getenv("AWS_LOCAL_IPV4")

// CORS
var MOONSTREAM_CORS_ALLOWED_ORIGINS = os.Getenv("MOONSTREAM_CORS_ALLOWED_ORIGINS")
