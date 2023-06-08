#!/usr/bin/env sh

# Sets up Brood server for docker compose:
# 1. Running alembic migrations to head (using config file specified 
# by the ALEMBIC_CONFIG environment variable)
# 2. Running dev.sh (from the directory from which this script was called)

set -e

if [ -z "$ALEMBIC_CONFIG" ]
then
    echo "Please explicitly set the ALEMBIC_CONFIG environment variable to point to an alembic configuration file"
    exit 1
fi

ALEMBIC_CONFIG="$ALEMBIC_CONFIG" sh alembic.sh upgrade head
