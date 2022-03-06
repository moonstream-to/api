package cmd

import (
	"encoding/json"
	"fmt"

	"github.com/bugout-dev/humbug/go/pkg"
	"github.com/bugout-dev/moonstream/crawlers/ldb/configs"
)

var (
	humbugReporter *HumbugReporter
)

// Generate humbug client
func setHumbugClient(sessionID string) error {
	consent := humbug.CreateHumbugConsent(humbug.True)
	reporter, err := humbug.CreateHumbugReporter(consent, configs.HUMBUG_LDB_CLIENT_ID, sessionID, configs.HUMBUG_LDB_TOKEN)
	if err != nil {
		return fmt.Errorf("Unable to generate humbug reporter: %v", err)
	}
	humbugReporter.Reporter = reporter

	return nil
}

func (r *HumbugReporter) submitReport(start, end uint64) error {
	content, err := json.Marshal(corruptBlocks)
	if err != nil {
		return fmt.Errorf("Unable to marshal to json: %v", err)
	}

	report := humbug.Report{
		Title:   fmt.Sprintf("LDB verifier %d-%d", start, end),
		Content: string(content),
		Tags: []string{
			fmt.Sprintf("start:%d", start),
			fmt.Sprintf("end:%d", end),
		},
	}
	r.Reporter.Publish(report)
	fmt.Printf("Error for range %d-%d published\n", start, end)

	return nil
}
