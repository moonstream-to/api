package main

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

func CreateDbPool(ctx context.Context, dbUri string, timeout string) (*pgxpool.Pool, error) {
	conf, err := pgxpool.ParseConfig(dbUri)
	if err != nil {
		return nil, fmt.Errorf("unable to parse database connection string, err: %v", err)
	}
	ctDuration, err := time.ParseDuration(timeout)
	if err != nil {
		return nil, fmt.Errorf("unable to parse connect timeout duration, err: %v", err)
	}
	conf.ConnConfig.ConnectTimeout = ctDuration

	dbPool, err := pgxpool.NewWithConfig(ctx, conf)
	if err != nil {
		return nil, fmt.Errorf("Unable to establish connection with database, err: %v", err)
	}

	return dbPool, nil
}
