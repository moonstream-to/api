package cmd

import (
	"database/sql"
	"log"

	_ "github.com/lib/pq"

	settings "github.com/bugout-dev/moonstream/db/server/configs"
)

func InitDB() *sql.DB {
	db, err := sql.Open("postgres", settings.MOONSTREAM_DB_URI_READ_ONLY)
	if err != nil {
		// DSN parse error or another initialization error
		log.Fatal(err)
	}

	// Set the maximum number of concurrently idle connections,
	// by default sql.DB allows a maximum of 2 idle connections.
	db.SetMaxIdleConns(settings.MOONSTREAM_DB_MAX_IDLE_CONNS)

	// Set the maximum lifetime of a connection.
	// Longer lifetime increase memory usage.
	db.SetConnMaxLifetime(settings.MOONSTREAM_DB_CONN_MAX_LIFETIME)

	return db
}
