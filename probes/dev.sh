#!/usr/bin/env sh

# Compile application and run with provided arguments
set -e

PROGRAM_NAME="probes_dev"

go build -o "$PROGRAM_NAME" cmd/probes/*.go

./"$PROGRAM_NAME" "$@"
