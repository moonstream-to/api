#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream database server

# Main
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
APP_DB_SERVER_DIR="${APP_DIR}/moonstreamdb/server"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
SCRIPT_DIR="$(realpath $(dirname $0))"
SERVICE_FILE="${SCRIPT_DIR}/moonstreamdb.service"

set -eu

echo
echo
echo "Retrieving deployment parameters for GCL Secret Manager"
mkdir -p "${SECRETS_DIR}"
echo "" > "${SECRETS_DIR}/app.env"
SECRET_NAMES=$(gcloud beta secrets list --filter="labels.product=moonstream" --format="get(name)")
for secret in $SECRET_NAMES
do
    secret_key=$(echo "${secret}" | awk -F'/' '{print $NF}')
    secret_val=$(gcloud secrets versions access latest --secret="${secret_key}")
    echo "${secret_key}=\"${secret_val}\"" >> "${SECRETS_DIR}/app.env"
done

echo
echo
echo "Building executable database server script with Go"
EXEC_DIR=$(pwd)
cd "${APP_DB_SERVER_DIR}"
HOME=/root /usr/local/go/bin/go build -o "${APP_DB_SERVER_DIR}/moonstreamdb" "${APP_DB_SERVER_DIR}/main.go"
cd "${EXEC_DIR}"

echo
echo
echo "Replacing existing moonstreamdb service definition with ${SERVICE_FILE}"
chmod 644 "${SERVICE_FILE}"
cp "${SERVICE_FILE}" /etc/systemd/system/moonstreamdb.service
systemctl daemon-reload
systemctl restart moonstreamdb.service
systemctl status moonstreamdb.service
