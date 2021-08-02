#!/usr/bin/env bash

TIMESTAMP="$(date +%s)"
SCRIPT_DIR=$(realpath $(dirname $0))

API_URL="${MOONSTREAM_DEV_API_URL:-http://localhost:7481}"

MOONSTREAM_USERNAME="devuser_$TIMESTAMP"
MOONSTREAM_PASSWORD="peppercat"
MOONSTREAM_EMAIL="devuser_$TIMESTAMP@example.com"

OUTPUT_DIR=$(mktemp -d)
echo "Writing responses to directory: $OUTPUT_DIR"

# Create a new user
curl -X POST \
    -H "Content-Type: multipart/form-data" \
    "$API_URL/users/" \
    -F "username=$MOONSTREAM_USERNAME" \
    -F "password=$MOONSTREAM_PASSWORD" \
    -F "email=$MOONSTREAM_EMAIL" \
    -o $OUTPUT_DIR/user.json

# Create a token for this user
curl -X POST \
    -H "Content-Type: multipart/form-data" \
    "$API_URL/users/token" \
    -F "username=$MOONSTREAM_USERNAME" \
    -F "password=$MOONSTREAM_PASSWORD" \
    -o $OUTPUT_DIR/token.json

API_TOKEN=$(jq -r '.id' $OUTPUT_DIR/token.json)

set -e

ETHEREUM_TXINFO_REQUEST_BODY_JSON=$(jq -r . $SCRIPT_DIR/txinfo_ethereum_blockchain_request.json)
curl -f -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_TOKEN" \
    "$API_URL/txinfo/ethereum_blockchain" \
    -d "$ETHEREUM_TXINFO_REQUEST_BODY_JSON" \
    -o $OUTPUT_DIR/txinfo_response.json

echo "Response:"
jq . $OUTPUT_DIR/txinfo_response.json

if [ "$DEBUG" != true ]
then
    echo "Deleting output directory: $OUTPUT_DIR"
    echo "Please set DEBUG=true if you would prefer to retain this directory in the future"
    rm -r $OUTPUT_DIR
fi