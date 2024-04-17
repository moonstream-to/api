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
SCRIPT_DIR="$(realpath $(dirname $0))"

# Ethereum service files
ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="ethereum-historical-crawl-transactions.service"
ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="ethereum-historical-crawl-transactions.timer"
ETHEREUM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="ethereum-historical-crawl-events.service"
ETHEREUM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="ethereum-historical-crawl-events.timer"

# Polygon service files
POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="polygon-historical-crawl-transactions.service"
POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="polygon-historical-crawl-transactions.timer"
POLYGON_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="polygon-historical-crawl-events.service"
POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="polygon-historical-crawl-events.timer"

# Amoy service files
AMOY_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="amoy-historical-crawl-transactions.service"
AMOY_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="amoy-historical-crawl-transactions.timer"
AMOY_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="amoy-historical-crawl-events.service"
AMOY_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="amoy-historical-crawl-events.timer"

# XDai service files
XDai_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="xdai-historical-crawl-transactions.service"
XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="xdai-historical-crawl-transactions.timer"
XDai_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="xdai-historical-crawl-events.service"
XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="xdai-historical-crawl-events.timer"

# ZkSync Era
ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="zksync-era-historical-crawl-transactions.service"
ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="zksync-era-historical-crawl-transactions.timer"
ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="zksync-era-historical-crawl-events.service"
ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="zksync-era-historical-crawl-events.timer"

# ZkSync Era Sepolia
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="zksync-era-sepolia-historical-crawl-transactions.service"
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="zksync-era-sepolia-historical-crawl-transactions.timer"
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="zksync-era-sepolia-historical-crawl-events.service"
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="zksync-era-sepolia-historical-crawl-events.timer"

# ProofofPlay APEX
PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="proofofplay-apex-historical-crawl-transactions.service"
PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="proofofplay-apex-historical-crawl-transactions.timer"
PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="proofofplay-apex-historical-crawl-events.service"
PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="proofofplay-apex-historical-crawl-events.timer"

set -eu

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
echo -e "${PREFIX_INFO} Install checkenv"
HOME=/home/ubuntu /usr/local/go/bin/go install github.com/bugout-dev/checkenv@latest

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
if [ ! -d "${SECRETS_DIR}" ]; then
  mkdir -p "${SECRETS_DIR}"
  echo -e "${PREFIX_WARN} Created new secrets directory"
fi
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" CHECKENV_AWS_FETCH_LOOP_LIMIT=20 /home/ubuntu/go/bin/checkenv show aws_ssm+moonstream:true > "${PARAMETERS_ENV_PATH}"
chmod 0640 "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Add instance local IP to parameters"
echo "AWS_LOCAL_IPV4=$(ec2metadata --local-ipv4)" >> "${PARAMETERS_ENV_PATH}"

echo
echo
if [ ! -d "/home/ubuntu/.config/systemd/user/" ]; then
  mkdir -p /home/ubuntu/.config/systemd/user/
  echo -e "${PREFIX_WARN} Created user systemd directory"
fi

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum historical transactions crawler service and timer with: ${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum historical events crawler service and timer with: ${ETHEREUM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${ETHEREUM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon historical transactions crawler service and timer with: ${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user  restart --no-block "${POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon historical events crawler service and timer with: ${POLYGON_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Amoy historical transactions crawler service and timer with: ${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AMOY_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Amoy historical events crawler service and timer with: ${AMOY_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${AMOY_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AMOY_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000"  systemctl --user restart --no-block "${AMOY_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing xDai historical transactions crawler service and timer with: ${XDai_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XDai_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing xDai historical events crawler service and timer with: ${XDai_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XDai_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000"  systemctl --user restart --no-block "${XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era historical transactions crawler service and timer with: ${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era historical events crawler service and timer with: ${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era Sepolia historical transactions crawler service and timer with: ${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era Sepolia historical events crawler service and timer with: ${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Proofofplay Apex historical transactions crawler service and timer with: ${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Proofofplay Apex historical events crawler service and timer with: ${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${PROOFOFPLAY_APEX_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
