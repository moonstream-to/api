#!/usr/bin/env sh

# Sets up Moonstream API server
# Expects access to Python environment with the requirements 
# for this project installed.
set -e

MOONSTREAMAPI_HOST="${MOONSTREAMAPI_HOST:-127.0.0.1}"
MOONSTREAMAPI_PORT="${MOONSTREAMAPI_PORT:-7481}"
MOONSTREAMAPI_APP_DIR="${MOONSTREAMAPI_APP_DIR:-$PWD}"
MOONSTREAMAPI_ASGI_APP="${MOONSTREAMAPI_ASGI_APP:-moonstreamapi.api:app}"
MOONSTREAMAPI_UVICORN_WORKERS="${MOONSTREAMAPI_UVICORN_WORKERS:-2}"

uvicorn --reload \
  --port "$MOONSTREAMAPI_PORT" \
  --host "$MOONSTREAMAPI_HOST" \
  --app-dir "$MOONSTREAMAPI_APP_DIR" \
  --workers "$MOONSTREAMAPI_UVICORN_WORKERS" \
  "$MOONSTREAMAPI_ASGI_APP"