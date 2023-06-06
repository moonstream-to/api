package cmd

type PingResponse struct {
	Status string `json:"status"`
}

type BlockLatestResponse struct {
	EthereumBlockLatest                   uint64 `json:"ethereum_block_latest"`
	PolygonBlockLatest                    uint64 `json:"polygon_block_latest"`
	PolygonBlockLatestLabelsMoonwormAlpha uint64 `json:"polygon_block_latest_label_moonworm_alpha"`
}
