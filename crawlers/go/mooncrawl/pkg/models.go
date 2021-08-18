package mooncrawl

type PendingTransaction struct {
	Hash        string `json:"hash`
	BlockNumber int    `json:"block_number"`
	FromAddress string `json:"from_address"`
	ToAddress   string `json:"to_address"`
	Gas         uint64 `json:"gas"`
	GasPrice    uint64 `json:"gas_price"`
	Input       string `json:"input"`
	Nonce       string `json:"nonce"`
	Value       uint64 `json:"value"`
}
