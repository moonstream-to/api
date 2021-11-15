#!/usr/bin/env sh

# Expects access to Python environment with the requirements for this project installed.
set -e

MOONSTREAM_HOST="${MOONSTREAM_HOST:-0.0.0.0}"
MOONSTREAM_PORT="${MOONSTREAM_PORT:-7491}"

uvicorn --port "$MOONSTREAM_PORT" --host "$MOONSTREAM_HOST" mooncrawl.api:app --reload
