#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream crawlers server

# Main
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
APP_CRAWLERS_DIR="${APP_DIR}/crawlers"
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/moonstream-env}"
PYTHON="${PYTHON_ENV_DIR}/bin/python"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"
AWS_SSM_PARAMETER_PATH="${AWS_SSM_PARAMETER_PATH:-/moonstream/prod}"
SCRIPT_DIR="$(realpath $(dirname $0))"
PARAMETERS_SCRIPT="${SCRIPT_DIR}/parameters.py"
ETHEREUM_TRENDING_SERVICE="ethereum-trending.service"
ETHEREUM_TRENDING_TIMER="ethereum-trending.service"
ETHEREUM_TXPOOL_SERVICE="ethereum-txpool.service"

set -eu

echo
echo
echo "Building executable Ethereum transaction pool crawler script with Go"
HOME=/root /usr/local/go/bin/go build -o "${APP_CRAWLERS_DIR}/ethtxpool/ethtxpool" "${APP_CRAWLERS_DIR}/ethtxpool/main.go"

echo
echo
echo "Updating Python dependencies"
"${PIP}" install --upgrade pip
"${PIP}" install -r "${APP_CRAWLERS_DIR}/mooncrawl/requirements.txt"

echo
echo
echo "Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" "${PYTHON}" "${PARAMETERS_SCRIPT}" extract -p "${AWS_SSM_PARAMETER_PATH}" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo "Replacing existing Ethereum trending service and timer with: ${ETHEREUM_TRENDING_SERVICE}, ${ETHEREUM_TRENDING_TIMER}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE}" "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE}" "/etc/systemd/system/${ETHEREUM_TRENDING_SERVICE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER}" "/etc/systemd/system/${ETHEREUM_TRENDING_TIMER}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_TRENDING_TIMER}"

echo
echo
echo "Replacing existing Ethereum transaction pool crawler service definition with ${ETHEREUM_TXPOOL_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE}" "/etc/systemd/system/${ETHEREUM_TXPOOL_SERVICE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_TXPOOL_SERVICE}"
