#!/usr/bin/env bash

# Deployment script - intended to run on Robots server

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
APP_DIR="${APP_DIR:-/home/ubuntu/api/robots}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
SCRIPT_DIR="$(realpath $(dirname $0))"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/robots-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"

# Airdrop service
ROBOTS_AIRDROP_SERVICE_FILE="robots-airdrop.service"

set -eu

if [ ! -d "$SECRETS_DIR" ]; then
  echo -e "${PREFIX_WARN} Created new directory for environment variables"
  mkdir "$SECRETS_DIR"
fi

echo
echo
echo -e "${PREFIX_INFO} Install checkenv"
HOME=/home/ubuntu /usr/local/go/bin/go install github.com/bugout-dev/checkenv@latest

echo
echo
echo -e "${PREFIX_INFO} Retrieving addition deployment parameters"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" /home/ubuntu/go/bin/checkenv show aws_ssm+robots:true > "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Building executable robots script with Go"
EXEC_DIR=$(pwd)
cd "${APP_DIR}"
HOME=/home/ubuntu /usr/local/go/bin/go build -o "${APP_DIR}/robots" "${APP_DIR}/cmd/robots/"
cd "${EXEC_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Airdrop robots service definition with ${ROBOTS_AIRDROP_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ROBOTS_AIRDROP_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ROBOTS_AIRDROP_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ROBOTS_AIRDROP_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart "${ROBOTS_AIRDROP_SERVICE_FILE}"
