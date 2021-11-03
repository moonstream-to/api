package cmd

type PingResponse struct {
	Status string `json:"status"`
}

type GethResponse struct {
	Result string `json:"result"`
}

type PingGethResponse struct {
	CurrentBlock uint64 `json:"current_block"`
}
