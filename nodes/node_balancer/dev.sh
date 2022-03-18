#!/usr/bin/env sh

# Colpile application and run with provided arguments
set -e

PROGRAM_NAME="nodebalancer"

go build -o "$PROGRAM_NAME" .

./"$PROGRAM_NAME" "$@"
