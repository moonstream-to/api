#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream servers

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
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
APP_BACKEND_DIR="${APP_DIR}/backend"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/moonstream-env}"
PYTHON="${PYTHON_ENV_DIR}/bin/python"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SCRIPT_DIR="$(realpath $(dirname $0))"
PARAMETERS_SCRIPT="${SCRIPT_DIR}/parameters.py"
PARAMETERS_BASH_SCRIPT="${SCRIPT_DIR}/parameters.bash"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"
AWS_SSM_PARAMETER_PATH="${AWS_SSM_PARAMETER_PATH:-/moonstream/prod}"
SERVICE_FILE="${SCRIPT_DIR}/moonstream.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Updating pip and setuptools"
"${PIP}" install -U pip setuptools

echo
echo
echo -e "${PREFIX_INFO} Updating Python dependencies"
"${PIP}" install -r "${APP_BACKEND_DIR}/requirements.txt"

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" "${PYTHON}" "${PARAMETERS_SCRIPT}" "${AWS_SSM_PARAMETER_PATH}" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Retrieving addition deployment parameters"
bash "${PARAMETERS_BASH_SCRIPT}" -p "moonstream" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Moonstream service definition with ${SERVICE_FILE}"
chmod 644 "${SERVICE_FILE}"
cp "${SERVICE_FILE}" /etc/systemd/system/moonstream.service
systemctl daemon-reload
systemctl restart moonstream.service
systemctl status moonstream.service
