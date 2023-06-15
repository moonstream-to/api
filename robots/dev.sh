#!/usr/bin/env sh

# Compile application and run with provided arguments
set -e

PROGRAM_NAME="robots_dev"

go build -o "$PROGRAM_NAME" cmd/robots/*.go

./"$PROGRAM_NAME" "$@"
