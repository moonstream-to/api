#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream crawlers server

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
APP_CRAWLERS_DIR="${APP_DIR}/crawlers"
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

# Ethereum service files
ETHEREUM_SYNCHRONIZE_SERVICE="ethereum-synchronize.service"
ETHEREUM_TRENDING_SERVICE_FILE="ethereum-trending.service"
ETHEREUM_TRENDING_TIMER_FILE="ethereum-trending.timer"
ETHEREUM_TXPOOL_SERVICE_FILE="ethereum-txpool.service"
ETHEREUM_MISSING_SERVICE_FILE="ethereum-missing.service"
ETHEREUM_MISSING_TIMER_FILE="ethereum-missing.timer"

# Polygon service file
POLYGON_SYNCHRONIZE_SERVICE="polygon-synchronize.service"
POLYGON_MISSING_SERVICE_FILE="polygon-missing.service"
POLYGON_MISSING_TIMER_FILE="polygon-missing.timer"
POLYGON_STATISTICS_SERVICE_FILE="polygon-statistics.service"
POLYGON_STATISTICS_TIMER_FILE="polygon-statistics.timer"
POLYGON_TXPOOL_SERVICE_FILE="polygon-txpool.service"


set -eu

echo
echo
echo -e "${PREFIX_INFO} Building executable Ethereum transaction pool crawler script with Go"
EXEC_DIR=$(pwd)
cd "${APP_CRAWLERS_DIR}/txpool"
HOME=/root /usr/local/go/bin/go build -o "${APP_CRAWLERS_DIR}/txpool/txpool" "${APP_CRAWLERS_DIR}/txpool/main.go"
cd "${EXEC_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Upgrading Python pip and setuptools"
"${PIP}" install --upgrade pip setuptools

echo
echo
echo -e "${PREFIX_INFO} Installing Python dependencies"
"${PIP}" install -e "${APP_CRAWLERS_DIR}/mooncrawl/"

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
echo -e "${PREFIX_INFO} Replacing existing Ethereum block with transactions syncronizer service definition with ${ETHEREUM_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ETHEREUM_SYNCHRONIZE_SERVICE}" "/etc/systemd/system/${ETHEREUM_SYNCHRONIZE_SERVICE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum trending service and timer with: ${ETHEREUM_TRENDING_SERVICE_FILE}, ${ETHEREUM_TRENDING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE_FILE}" "/etc/systemd/system/${ETHEREUM_TRENDING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER_FILE}" "/etc/systemd/system/${ETHEREUM_TRENDING_TIMER_FILE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_TRENDING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum transaction pool crawler service definition with ${ETHEREUM_TXPOOL_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE_FILE}" "/etc/systemd/system/${ETHEREUM_TXPOOL_SERVICE_FILE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_TXPOOL_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum missing service and timer with: ${ETHEREUM_MISSING_SERVICE_FILE}, ${ETHEREUM_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_MISSING_SERVICE_FILE}" "/etc/systemd/system/${ETHEREUM_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_MISSING_TIMER_FILE}" "/etc/systemd/system/${ETHEREUM_MISSING_TIMER_FILE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon block with transactions syncronizer service definition with ${POLYGON_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${POLYGON_SYNCHRONIZE_SERVICE}" "/etc/systemd/system/${POLYGON_SYNCHRONIZE_SERVICE}"
systemctl daemon-reload
systemctl restart "${POLYGON_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon missing service and timer with: ${POLYGON_MISSING_SERVICE_FILE}, ${POLYGON_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_MISSING_SERVICE_FILE}" "/etc/systemd/system/${POLYGON_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_MISSING_TIMER_FILE}" "/etc/systemd/system/${POLYGON_MISSING_TIMER_FILE}"
systemctl daemon-reload
systemctl restart "${POLYGON_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon statistics dashbord service and timer with: ${POLYGON_STATISTICS_SERVICE_FILE}, ${POLYGON_STATISTICS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_STATISTICS_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_STATISTICS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATISTICS_SERVICE_FILE}" "/etc/systemd/system/${POLYGON_STATISTICS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATISTICS_TIMER_FILE}" "/etc/systemd/system/${POLYGON_STATISTICS_TIMER_FILE}"
systemctl daemon-reload
systemctl restart "${POLYGON_STATISTICS_TIMER_FILE}"

# echo
# echo
# echo -e "${PREFIX_INFO} Replacing existing Polygon transaction pool crawler service definition with ${POLYGON_TXPOOL_SERVICE_FILE}"
# chmod 644 "${SCRIPT_DIR}/${POLYGON_TXPOOL_SERVICE_FILE}"
# cp "${SCRIPT_DIR}/${POLYGON_TXPOOL_SERVICE_FILE}" "/etc/systemd/system/${POLYGON_TXPOOL_SERVICE_FILE}"
# systemctl daemon-reload
# systemctl restart "${POLYGON_TXPOOL_SERVICE_FILE}"
