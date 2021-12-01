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
	MOONSTREAM_NODE_IPC_ADDR := os.Getenv(fmt.Sprintf("MOONSTREAM_NODE_%s_IPC_ADDR", strings.ToUpper(blockchain)))
	MOONSTREAM_NODE_IPC_PORT := os.Getenv(fmt.Sprintf("MOONSTREAM_NODE_%s_IPC_PORT", strings.ToUpper(blockchain)))
	return fmt.Sprintf("http://%s:%s", MOONSTREAM_NODE_IPC_ADDR, MOONSTREAM_NODE_IPC_PORT)
}
