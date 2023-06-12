package probs

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
)

type ServiceWorker struct {
	Name           string `json:"name"`
	Description    string
	LonDescription string
	Interval       int `json:"interval"`

	ExecFunction func(context.Context, *pgxpool.Pool) error
}
