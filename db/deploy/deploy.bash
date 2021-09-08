#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream database server

# Main
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
APP_DB_SERVER_DIR="${APP_DIR}/db/server"
SCRIPT_DIR="$(realpath $(dirname $0))"
SERVICE_FILE="${SCRIPT_DIR}/moonstreamdb.service"

echo
echo
echo "Building executable database server script with Go"
/usr/local/go/bin/go build -o "${APP_DB_SERVER_DIR}/moonstreamdb" "${APP_DB_SERVER_DIR}/main.go"

echo
echo
echo "Replacing existing moonstreamdb service definition with ${SERVICE_FILE}"
chmod 644 "${SERVICE_FILE}"
cp "${SERVICE_FILE}" /etc/systemd/system/moonstreamdb.service
systemctl daemon-reload
systemctl restart moonstreamdb.service
systemctl status moonstreamdb.service
