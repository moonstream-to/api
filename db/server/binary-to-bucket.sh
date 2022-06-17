#!/usr/bin/env sh

# Compile application and put to S3 bugout-binaries bucket
set -e

PROGRAM_NAME="moonstreamdb"

go build -o "$PROGRAM_NAME" .

sha256sum moonstreamdb > moonstreamdb.checksum

aws s3 cp "$PROGRAM_NAME" "s3://bugout-binaries-public/prod/moonstream/db/$PROGRAM_NAME"
