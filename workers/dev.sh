#!/usr/bin/env sh

# Compile application and run with provided arguments
set -e

PROGRAM_NAME="workers_dev"

go build -o "$PROGRAM_NAME" cmd/workers/*.go

./"$PROGRAM_NAME" "$@"
