#!/usr/bin/env bash

# Deployment script

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
APP_DIR="${APP_DIR:-/home/ubuntu/api/engineapi}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/engineapi-env}"
PYTHON="${PYTHON_ENV_DIR}/bin/python"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SCRIPT_DIR="$(realpath $(dirname $0))"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/engineapi-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"

# API server service file
ENGINE_SERVICE_FILE="engine.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Upgrading Python pip and setuptools"
"${PIP}" install --upgrade pip setuptools

echo
echo
echo -e "${PREFIX_INFO} Installing Python dependencies"
"${PIP}" install --exists-action i -r "${APP_DIR}/requirements.txt"

echo
echo
echo -e "${PREFIX_INFO} Install checkenv"
HOME=/home/ubuntu /usr/local/go/bin/go install github.com/bugout-dev/checkenv@latest

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
if [ ! -d "${SECRETS_DIR}" ]; then
  mkdir "${SECRETS_DIR}"
  echo -e "${PREFIX_WARN} Created new secrets directory"
fi
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" /home/ubuntu/go/bin/checkenv show aws_ssm+engine:true > "${PARAMETERS_ENV_PATH}"
chmod 0640 "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Add AWS default region to parameters"
echo "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" >> "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Add instance local IP to parameters"
echo "AWS_LOCAL_IPV4=$(ec2metadata --local-ipv4)" >> "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Engine API server service definition with ${ENGINE_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ENGINE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ENGINE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ENGINE_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ENGINE_SERVICE_FILE}"
