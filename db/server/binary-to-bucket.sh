#!/usr/bin/env sh

# Compile application and put to S3 bugout-binaries bucket
set -e

PROGRAM_NAME="moonstreamdb"

go build -o "$PROGRAM_NAME" .

aws s3 cp "$PROGRAM_NAME" "s3://bugout-binaries/prod/moonstream/db/$PROGRAM_NAME"
