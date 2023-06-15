#!/usr/bin/env sh

# Expects access to Python environment with the requirements
# for this project installed.
set -e

ENGINE_HOST="${ENGINE_HOST:-127.0.0.1}"
ENGINE_PORT="${ENGINE_PORT:-7191}"
ENGINE_WORKERS="${ENGINE_WORKERS:-1}"

uvicorn --port "$ENGINE_PORT" --host "$ENGINE_HOST" --workers "$ENGINE_WORKERS" engineapi.api:app
