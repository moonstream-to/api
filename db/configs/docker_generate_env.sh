#!/usr/bin/env sh

# Prepare Moonstream DB application for docker-compose use

set -e

SCRIPT_DIR="$(realpath $(dirname $0))"
DOCKER_MOONSTREAMDB_DB_URI="postgresql://postgres:postgres@db/moonstream_dev"
DOCKER_MOONSTREAMDB_ENV_FILE="docker.moonstreamdb.env"
DOCKER_MOONSTREAMDB_ALEMBIC_FILE="alembic.moonstreamdb.ini"

# Generate environment variables

cp "$SCRIPT_DIR/sample.env" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"

# Clean file with variables from export prefix and quotation marks
sed --in-place 's|^export * ||' "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"
sed --in-place 's|"||g' "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"

sed -i "s|^MOONSTREAM_DB_URI=.*|MOONSTREAM_DB_URI=$DOCKER_MOONSTREAMDB_DB_URI|" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"

# Generate alembic config

cp "$SCRIPT_DIR/alembic.sample.ini" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ALEMBIC_FILE"

sed -i "s|^sqlalchemy.url =.*|sqlalchemy.url = $DOCKER_MOONSTREAMDB_DB_URI|" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ALEMBIC_FILE"
