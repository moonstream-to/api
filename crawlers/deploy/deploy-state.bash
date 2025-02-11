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
ETHEREUM_STATE_SERVICE_FILE="ethereum-state.service"
ETHEREUM_STATE_TIMER_FILE="ethereum-state.timer"
ETHEREUM_STATE_CLEAN_SERVICE_FILE="ethereum-state-clean.service"
ETHEREUM_STATE_CLEAN_TIMER_FILE="ethereum-state-clean.timer"
ETHEREUM_METADATA_SERVICE_FILE="ethereum-metadata.service"
ETHEREUM_METADATA_TIMER_FILE="ethereum-metadata.timer"

# Ethereum Sepolia
SEPOLIA_STATE_SERVICE_FILE="sepolia-state.service"
SEPOLIA_STATE_TIMER_FILE="sepolia-state.timer"

# Polygon service files
POLYGON_STATE_SERVICE_FILE="polygon-state.service"
POLYGON_STATE_TIMER_FILE="polygon-state.timer"
POLYGON_STATE_CLEAN_SERVICE_FILE="polygon-state-clean.service"
POLYGON_STATE_CLEAN_TIMER_FILE="polygon-state-clean.timer"
POLYGON_METADATA_SERVICE_FILE="polygon-metadata.service"
POLYGON_METADATA_TIMER_FILE="polygon-metadata.timer"

# ZkSync Era
ZKSYNC_ERA_STATE_SERVICE_FILE="zksync-era-state.service"
ZKSYNC_ERA_STATE_TIMER_FILE="zksync-era-state.timer"
ZKSYNC_ERA_STATE_CLEAN_SERVICE_FILE="zksync-era-state-clean.service"
ZKSYNC_ERA_STATE_CLEAN_TIMER_FILE="zksync-era-state-clean.timer"

# Arbitrum one
ARBITRUM_ONE_STATE_SERVICE_FILE="arbitrum-one-state.service"
ARBITRUM_ONE_STATE_TIMER_FILE="arbitrum-one-state.timer"

# Arbitrum Sepolia
ARBITRUM_SEPOLIA_STATE_SERVICE_FILE="arbitrum-sepolia-state.service"
ARBITRUM_SEPOLIA_STATE_TIMER_FILE="arbitrum-sepolia-state.timer"

# Xai
XAI_STATE_SERVICE_FILE="xai-state.service"
XAI_STATE_TIMER_FILE="xai-state.timer"
XAI_STATE_CLEAN_SERVICE_FILE="xai-state-clean.service"
XAI_STATE_CLEAN_TIMER_FILE="xai-state-clean.timer"
XAI_METADATA_SERVICE_FILE="xai-metadata.service"
XAI_METADATA_TIMER_FILE="xai-metadata.timer"

# Xai sepolia
XAI_SEPOLIA_STATE_SERVICE_FILE="xai-sepolia-state.service"
XAI_SEPOLIA_STATE_TIMER_FILE="xai-sepolia-state.timer"
XAI_SEPOLIA_STATE_CLEAN_SERVICE_FILE="xai-sepolia-state-clean.service"
XAI_SEPOLIA_STATE_CLEAN_TIMER_FILE="xai-sepolia-state-clean.timer"
XAI_SEPOLIA_METADATA_SERVICE_FILE="xai-sepolia-metadata.service"
XAI_SEPOLIA_METADATA_TIMER_FILE="xai-sepolia-metadata.timer"

# Game7
GAME7_METADATA_SERVICE_FILE="game7-metadata.service"
GAME7_METADATA_TIMER_FILE="game7-metadata.timer"
GAME7_STATE_SERVICE_FILE="game7-state.service"
GAME7_STATE_TIMER_FILE="game7-state.timer"
GAME7_STATE_CLEAN_SERVICE_FILE="game7-state-clean.service"
GAME7_STATE_CLEAN_TIMER_FILE="game7-state-clean.timer"

# Game7 testnet
GAME7_TESTNET_METADATA_SERVICE_FILE="game7-testnet-metadata.service"
GAME7_TESTNET_METADATA_TIMER_FILE="game7-testnet-metadata.timer"
GAME7_TESTNET_STATE_SERVICE_FILE="game7-testnet-state.service"
GAME7_TESTNET_STATE_TIMER_FILE="game7-testnet-state.timer"


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
HOME=/home/ubuntu /usr/local/go/bin/go install github.com/bugout-dev/checkenv@v0.0.4

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
if [ ! -d "${SECRETS_DIR}" ]; then
  mkdir -p "${SECRETS_DIR}"
  echo -e "${PREFIX_WARN} Created new secrets directory"
fi
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" CHECKENV_AWS_FETCH_LOOP_LIMIT=20 /home/ubuntu/go/bin/checkenv show aws_ssm+moonstream:true > "${PARAMETERS_ENV_PATH}"
MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_CRAWLERS=$(AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" aws ssm get-parameter --name "MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_CRAWLERS" --output text --query Parameter.Value)
echo "MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS=$MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_CRAWLERS" >> "${PARAMETERS_ENV_PATH}"
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
echo -e "${PREFIX_INFO} Replacing existing Ethereum state service and timer with: ${ETHEREUM_STATE_SERVICE_FILE}, ${ETHEREUM_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_STATE_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum state clean service and timer with: ${ETHEREUM_STATE_CLEAN_SERVICE_FILE}, ${ETHEREUM_STATE_CLEAN_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_STATE_CLEAN_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_STATE_CLEAN_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_STATE_CLEAN_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_STATE_CLEAN_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_STATE_CLEAN_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_STATE_CLEAN_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_STATE_CLEAN_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum metadata service and timer with: ${ETHEREUM_METADATA_SERVICE_FILE}, ${ETHEREUM_METADATA_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_METADATA_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_METADATA_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_METADATA_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_METADATA_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_METADATA_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_METADATA_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_METADATA_TIMER_FILE}"


# Ethereum Sepolia

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum Sepolia state service and timer with: ${SEPOLIA_STATE_SERVICE_FILE}, ${SEPOLIA_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${SEPOLIA_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${SEPOLIA_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${SEPOLIA_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${SEPOLIA_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${SEPOLIA_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${SEPOLIA_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${SEPOLIA_STATE_TIMER_FILE}"


# Polygon

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon state service and timer with: ${POLYGON_STATE_SERVICE_FILE}, ${POLYGON_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_STATE_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon state clean service and timer with: ${POLYGON_STATE_CLEAN_SERVICE_FILE}, ${POLYGON_STATE_CLEAN_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_STATE_CLEAN_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_STATE_CLEAN_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATE_CLEAN_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_STATE_CLEAN_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATE_CLEAN_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_STATE_CLEAN_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_STATE_CLEAN_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon metadata service and timer with: ${POLYGON_METADATA_SERVICE_FILE}, ${POLYGON_METADATA_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_METADATA_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_METADATA_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_METADATA_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_METADATA_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_METADATA_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_METADATA_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_METADATA_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era state service and timer with: ${ZKSYNC_ERA_STATE_SERVICE_FILE}, ${ZKSYNC_ERA_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000"  systemctl --user restart --no-block "${ZKSYNC_ERA_STATE_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era state clean service and timer with: ${ZKSYNC_ERA_STATE_CLEAN_SERVICE_FILE}, ${ZKSYNC_ERA_STATE_CLEAN_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_CLEAN_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_CLEAN_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_CLEAN_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_STATE_CLEAN_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_STATE_CLEAN_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_STATE_CLEAN_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000"  systemctl --user restart --no-block "${ZKSYNC_ERA_STATE_CLEAN_TIMER_FILE}"

# Arbitrum one

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum one state service and timer with: ${ARBITRUM_ONE_STATE_SERVICE_FILE}, ${ARBITRUM_ONE_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_ONE_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${ARBITRUM_ONE_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_ONE_STATE_TIMER_FILE}"


# Arbitrum Sepolia

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Sepolia state service and timer with: ${ARBITRUM_SEPOLIA_STATE_SERVICE_FILE}, ${ARBITRUM_SEPOLIA_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_SEPOLIA_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_SEPOLIA_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_SEPOLIA_STATE_TIMER_FILE}"


# Xai

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai state service and timer with: ${XAI_STATE_SERVICE_FILE}, ${XAI_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_STATE_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai state clean service and timer with: ${XAI_STATE_CLEAN_SERVICE_FILE}, ${XAI_STATE_CLEAN_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_STATE_CLEAN_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_STATE_CLEAN_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_STATE_CLEAN_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_STATE_CLEAN_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_STATE_CLEAN_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_STATE_CLEAN_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_STATE_CLEAN_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai metadata service and timer with: ${XAI_METADATA_SERVICE_FILE}, ${XAI_METADATA_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_METADATA_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_METADATA_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_METADATA_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_METADATA_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_METADATA_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_METADATA_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_METADATA_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia state service and timer with: ${XAI_SEPOLIA_STATE_SERVICE_FILE}, ${XAI_SEPOLIA_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_STATE_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia state clean service and timer with: ${XAI_SEPOLIA_STATE_CLEAN_SERVICE_FILE}, ${XAI_SEPOLIA_STATE_CLEAN_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_CLEAN_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_CLEAN_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_CLEAN_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_STATE_CLEAN_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_STATE_CLEAN_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_STATE_CLEAN_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_STATE_CLEAN_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia metadata service and timer with: ${XAI_SEPOLIA_METADATA_SERVICE_FILE}, ${XAI_SEPOLIA_METADATA_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_METADATA_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_SEPOLIA_METADATA_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_METADATA_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_METADATA_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_METADATA_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_METADATA_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_METADATA_TIMER_FILE}"

# Game7

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Game7 metadata service and timer with: ${GAME7_METADATA_SERVICE_FILE}, ${GAME7_METADATA_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${GAME7_METADATA_SERVICE_FILE}" "${SCRIPT_DIR}/${GAME7_METADATA_TIMER_FILE}"
cp "${SCRIPT_DIR}/${GAME7_METADATA_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_METADATA_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${GAME7_METADATA_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_METADATA_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${GAME7_METADATA_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Game7 state service and timer with: ${GAME7_STATE_SERVICE_FILE}, ${GAME7_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${GAME7_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${GAME7_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${GAME7_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${GAME7_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${GAME7_STATE_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Game7 state clean service and timer with: ${GAME7_STATE_CLEAN_SERVICE_FILE}, ${GAME7_STATE_CLEAN_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${GAME7_STATE_CLEAN_SERVICE_FILE}" "${SCRIPT_DIR}/${GAME7_STATE_CLEAN_TIMER_FILE}"
cp "${SCRIPT_DIR}/${GAME7_STATE_CLEAN_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_STATE_CLEAN_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${GAME7_STATE_CLEAN_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_STATE_CLEAN_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${GAME7_STATE_CLEAN_TIMER_FILE}"

# Game7 testnet

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Game7 testnet metadata service and timer with: ${GAME7_TESTNET_METADATA_SERVICE_FILE}, ${GAME7_TESTNET_METADATA_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${GAME7_TESTNET_METADATA_SERVICE_FILE}" "${SCRIPT_DIR}/${GAME7_TESTNET_METADATA_TIMER_FILE}"
cp "${SCRIPT_DIR}/${GAME7_TESTNET_METADATA_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_TESTNET_METADATA_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${GAME7_TESTNET_METADATA_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_TESTNET_METADATA_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${GAME7_TESTNET_METADATA_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Game7 testnet state service and timer with: ${GAME7_TESTNET_STATE_SERVICE_FILE}, ${GAME7_TESTNET_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${GAME7_TESTNET_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${GAME7_TESTNET_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${GAME7_TESTNET_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_TESTNET_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${GAME7_TESTNET_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${GAME7_TESTNET_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${GAME7_TESTNET_STATE_TIMER_FILE}"
