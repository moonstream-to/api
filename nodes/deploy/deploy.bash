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
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
APP_NODES_DIR="${APP_DIR}/nodes"
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/moonstream-env}"
PYTHON="${PYTHON_ENV_DIR}/bin/python"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"
AWS_SSM_PARAMETER_PATH="${AWS_SSM_PARAMETER_PATH:-/moonstream/prod}"
SCRIPT_DIR="$(realpath $(dirname $0))"

# Parameters scripts
PARAMETERS_SCRIPT="${SCRIPT_DIR}/parameters.py"
CHECKENV_PARAMETERS_SCRIPT="${SCRIPT_DIR}/parameters.bash"
CHECKENV_NODES_CONNECTIONS_SCRIPT="${SCRIPT_DIR}/nodes-connections.bash"

# Service file
NODE_BALANCER_SERVICE_FILE="node-balancer.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Building executable load balancer for nodes script with Go"
EXEC_DIR=$(pwd)
cd "${APP_NODES_DIR}/node_balancer"
HOME=/root /usr/local/go/bin/go build -o "${APP_NODES_DIR}/node_balancer/nodebalancer" "${APP_NODES_DIR}/node_balancer/main.go"
cd "${EXEC_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" "${PYTHON}" "${PARAMETERS_SCRIPT}" extract -p "${AWS_SSM_PARAMETER_PATH}" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Retrieving addition deployment parameters"
bash "${CHECKENV_PARAMETERS_SCRIPT}" -v -p "moonstream" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Updating nodes connection parameters"
bash "${CHECKENV_NODES_CONNECTIONS_SCRIPT}" -v -f "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing load balancer for nodes service definition with ${NODE_BALANCER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${NODE_BALANCER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${NODE_BALANCER_SERVICE_FILE}" "/etc/systemd/system/${NODE_BALANCER_SERVICE_FILE}"
systemctl daemon-reload
systemctl restart "${NODE_BALANCER_SERVICE_FILE}"
