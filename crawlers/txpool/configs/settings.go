package settings

import (
	"fmt"
	"os"
	"strings"
)

// Internal crash journal to collect errors
var HUMBUG_REPORTER_CRAWLERS_TOKEN = os.Getenv("HUMBUG_REPORTER_CRAWLERS_TOKEN")

var HUMBUG_TXPOOL_CLIENT_ID = os.Getenv("HUMBUG_TXPOOL_CLIENT_ID")
var HUMBUG_TXPOOL_TOKEN = os.Getenv("HUMBUG_TXPOOL_TOKEN")

// Geth connection URL
func GetIpcPath(blockchain string) string {
	MOONSTREAM_WEB3_PROVIDER_URI := os.Getenv(fmt.Sprintf("MOONSTREAM_%s_WEB3_PROVIDER_URI", strings.ToUpper(blockchain)))
	return MOONSTREAM_WEB3_PROVIDER_URI
}
