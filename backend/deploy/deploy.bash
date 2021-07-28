#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream servers

# Main
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/moonstream-env}"
PYTHON="${PYTHON_ENV_DIR}/bin/python"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SCRIPT_DIR="$(realpath $(dirname $0))"
PARAMETERS_SCRIPT="${SCRIPT_DIR}/parameters.py"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"
AWS_SSM_PARAMETER_PATH="${AWS_SSM_PARAMETER_PATH:-/moonstream/prod}"
SERVICE_FILE="${SCRIPT_DIR}/moonstream.service"

set -eu

echo
echo
echo "Updating pip and setuptools"
"${PIP}" install -U pip setuptools

echo
echo
echo "Updating Python dependencies"
"${PIP}" install -r "${APP_DIR}/requirements.txt"

echo
echo
echo "Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" "${PYTHON}" "${PARAMETERS_SCRIPT}" "${AWS_SSM_PARAMETER_PATH}" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo "Replacing existing Moonstream service definition with ${SERVICE_FILE}"
chmod 644 "${SERVICE_FILE}"
cp "${SERVICE_FILE}" /etc/systemd/system/moonstream.service
systemctl daemon-reload
systemctl restart moonstream.service
systemctl status moonstream.service
