#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream database server

# Main
SCRIPT_DIR="$(realpath $(dirname $0))"
SERVICE_FILE="${SCRIPT_DIR}/moonstreamdb.service"

echo
echo
echo "Replacing existing moonstreamdb service definition with ${SERVICE_FILE}"
chmod 644 "${SERVICE_FILE}"
cp "${SERVICE_FILE}" /etc/systemd/system/moonstreamdb.service
systemctl daemon-reload
systemctl restart moonstreamdb.service
systemctl status moonstreamdb.service
