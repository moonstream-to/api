#!/usr/bin/env bash

# Prepare Moonstream DB application for docker-compose use

# Print help message
function usage {
  echo "Usage: $0 [-h] -d DATABASE_NAME"  
  echo
  echo "CLI to generate environment variables"
  echo
  echo "Optional arguments:"
  echo "  -h  Show this help message and exit"
  echo "  -d  Database name for postgres in docker-compose setup"
}

FLAG_DATABASE_NAME="moonstream_dev"

while getopts 'd:' flag; do
  case "${flag}" in
    d) FLAG_DATABASE_NAME="${OPTARG}" ;;
    h) usage
      exit 1 ;;
    *) usage
      exit 1 ;;
  esac
done

set -e

SCRIPT_DIR="$(realpath $(dirname $0))"
DOCKER_MOONSTREAMDB_DB_URI="postgresql://postgres:postgres@db/$FLAG_DATABASE_NAME"
DOCKER_MOONSTREAMDB_ENV_FILE="docker.moonstreamdb.env"
DOCKER_MOONSTREAMDB_ALEMBIC_FILE="alembic.moonstreamdb.ini"

# Generate environment variables

cp "$SCRIPT_DIR/sample.env" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"

# Clean file with variables from export prefix and quotation marks
sed --in-place 's|^export * ||' "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"
sed --in-place 's|"||g' "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"

sed -i "s|^MOONSTREAM_DB_URI=.*|MOONSTREAM_DB_URI=$DOCKER_MOONSTREAMDB_DB_URI|" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"
sed -i "s|^MOONSTREAM_DB_URI_READ_ONLY=.*|MOONSTREAM_DB_URI_READ_ONLY=$DOCKER_MOONSTREAMDB_DB_URI|" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ENV_FILE"

# Generate alembic config

cp "$SCRIPT_DIR/alembic.sample.ini" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ALEMBIC_FILE"

sed -i "s|^sqlalchemy.url =.*|sqlalchemy.url = $DOCKER_MOONSTREAMDB_DB_URI|" "$SCRIPT_DIR/$DOCKER_MOONSTREAMDB_ALEMBIC_FILE"
