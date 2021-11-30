#!/usr/bin/env sh

# Prepare Moonstream API application for docker-compose use

set -e

SCRIPT_DIR="$(realpath $(dirname $0))"
DOCKER_MOONSTREAM_DB_URI="postgresql://postgres:postgres@db/moonstream_dev"
DOCKER_MOONSTREAM_ENV_FILE="docker.moonstreamapi.env"

# Generate environment variables

cp "$SCRIPT_DIR/sample.env" "$SCRIPT_DIR/$DOCKER_MOONSTREAM_ENV_FILE"

# Clean file with variables from export prefix and quotation marks
sed --in-place 's|^export * ||' "$SCRIPT_DIR/$DOCKER_MOONSTREAM_ENV_FILE"
sed --in-place 's|"||g' "$SCRIPT_DIR/$DOCKER_MOONSTREAM_ENV_FILE"

sed -i "s|^MOONSTREAM_DB_URI=.*|MOONSTREAM_DB_URI=$DOCKER_MOONSTREAM_DB_URI|" "$SCRIPT_DIR/$DOCKER_MOONSTREAM_ENV_FILE"
