package probes

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
)

type ApplicationProbe struct {
	Name           string `json:"name"`
	Description    string
	LonDescription string
	Interval       int `json:"interval"`

	ExecFunction func(context.Context, *pgxpool.Pool) error
}
