#!/usr/bin/env sh

# Compile application and run with provided arguments
set -e

PROGRAM_NAME="probs_dev"

go build -o "$PROGRAM_NAME" cmd/probs/*.go

./"$PROGRAM_NAME" "$@"
