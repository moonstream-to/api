package cmd

type PingResponse struct {
	Status string `json:"status"`
}

type BlockNumberResponse struct {
	BlockNumber uint64 `json:"block_number"`
}
