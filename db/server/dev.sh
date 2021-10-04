#!/usr/bin/env sh

# Expects access to Python environment with the requirements for this project installed.
set -e

MOONSTREAM_DB_SERVER_HOST="${MOONSTREAM_DB_SERVER_HOST:-0.0.0.0}"
MOONSTREAM_DB_SERVER_PORT="${MOONSTREAM_DB_SERVER_PORT:-8080}"

go run main.go -host "${MOONSTREAM_DB_SERVER_HOST}" -port "${MOONSTREAM_DB_SERVER_PORT}"
