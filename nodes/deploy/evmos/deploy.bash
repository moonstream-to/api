#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream Evmos node server

# Colors
C_RESET='\033[0m'
C_RED='\033[1;31m'
C_GREEN='\033[1;32m'
C_YELLOW='\033[1;33m'

# Logs
PREFIX_INFO="${C_GREEN}[INFO]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_WARN="${C_YELLOW}[WARN]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_CRIT="${C_RED}[CRIT]${C_RESET} [$(date +%d-%m\ %T)]"

# Main
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
APP_NODES_DIR="${APP_DIR}/nodes"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"
SCRIPT_DIR="$(realpath $(dirname $0))"

# Node status server service file
NODE_STATUS_SERVER_SERVICE_FILE="node-status.service"

# Evmos service file
EVMOS_NETHERMIND_SERVICE_FILE="evmos.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Building executable server of node status server"
EXEC_DIR=$(pwd)
cd "${APP_NODES_DIR}/server"
HOME=/root /usr/local/go/bin/go build -o "${APP_NODES_DIR}/server/nodestatus" "${APP_NODES_DIR}/server/main.go"
cd "${EXEC_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Create secrets directory"
mkdir -p "${SECRETS_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Install checkenv"
HOME=/root /usr/local/go/bin/go install github.com/bugout-dev/checkenv@latest

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" /root/go/bin/checkenv show aws_ssm+Product:moonstream,Node:true > "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Add instance local IP to parameters"
AWS_LOCAL_IPV4="$(ec2metadata --local-ipv4)"
echo "AWS_LOCAL_IPV4=$AWS_LOCAL_IPV4" >> "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing node status server definition with ${NODE_STATUS_SERVER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${NODE_STATUS_SERVER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${NODE_STATUS_SERVER_SERVICE_FILE}" "/etc/systemd/system/${NODE_STATUS_SERVER_SERVICE_FILE}"
systemctl daemon-reload
systemctl restart "${NODE_STATUS_SERVER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Evmos service definition with ${EVMOS_NETHERMIND_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${EVMOS_NETHERMIND_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${EVMOS_NETHERMIND_SERVICE_FILE}" "/etc/systemd/system/${EVMOS_NETHERMIND_SERVICE_FILE}"
systemctl daemon-reload
systemctl disable "${EVMOS_NETHERMIND_SERVICE_FILE}"
echo -e "${PREFIX_WARN} Evmos service updated, but not restarted!"
