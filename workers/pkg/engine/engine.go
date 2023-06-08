package engine

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

type CallRequest struct {
	Id                    string      `json:"id"`
	RegisteredContractIid string      `json:"registered_contract_id"`
	Caller                string      `json:"caller"`
	MoonstreamUserId      string      `json:"moonstream_user_id"`
	Method                string      `json:"method"`
	Parameters            interface{} `json:"parameters"`
	ExpiresAt             time.Time   `json:"expires_at"`
	CreatedAt             time.Time   `json:"created_at"`
	UpdatedAt             time.Time   `json:"updated_at"`
}

func CleanCallRequestsCommand(ctx context.Context, dbPool *pgxpool.Pool) error {
	tag, err := dbPool.Exec(
		ctx,
		"DELETE FROM call_requests WHERE expires_at <= NOW() - INTERVAL '1 minute';",
	)
	if err != nil {
		return fmt.Errorf("delete execution failed, err: %v", err)
	}

	log.Printf("Deleted %d call requests", tag.RowsAffected())
	return nil
}
