#!/usr/bin/env sh

set -e
  
HOST="$1"
shift

until curl --request GET --url "http://$HOST/ping"; do
  >&2 echo "$HOST is unavailable, sleeping"
  sleep 1
done

>&2 echo "$HOST is up"
