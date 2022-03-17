#!/usr/bin/env sh

PROGRAM_NAME="nodebalancer"

go build -o "$PROGRAM_NAME" .

./"$PROGRAM_NAME" "$@"
