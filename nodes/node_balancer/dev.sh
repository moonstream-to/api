#!/usr/bin/env sh

# Compile application and run with provided arguments
set -e

PROGRAM_NAME="nodebalancer"

go build -o "$PROGRAM_NAME" cmd/nodebalancer/*.go

./"$PROGRAM_NAME" "$@"
