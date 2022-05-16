#!/usr/bin/env sh

# Colpile application and run with provided arguments
set -e

PROGRAM_NAME="txpool"

go build -o "$PROGRAM_NAME" .

./"$PROGRAM_NAME" "$@"
