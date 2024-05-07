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

# Service files
ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE="ethereum-moonworm-crawler.service"
POLYGON_MOONWORM_CRAWLER_SERVICE_FILE="polygon-moonworm-crawler.service"
AMOY_MOONWORM_CRAWLER_SERVICE_FILE="amoy-moonworm-crawler.service"
XDAI_MOONWORM_CRAWLER_SERVICE_FILE="xdai-moonworm-crawler.service"
ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE="zksync-era-moonworm-crawler.service"
ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="zksync-era-sepolia-moonworm-crawler.service"
ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE="arbitrum-one-moonworm-crawler.service"
ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE="arbitrum-nova-moonworm-crawler.service"
ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="arbitrum-sepolia-moonworm-crawler.service"
XAI_MOONWORM_CRAWLER_SERVICE_FILE="xai-moonworm-crawler.service"
XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="xai-sepolia-moonworm-crawler.service"
AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE="avalanche-moonworm-crawler.service"
AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE="avalanche-fuji-moonworm-crawler.service"
BLAST_MOONWORM_CRAWLER_SERVICE_FILE="blast-moonworm-crawler.service"
BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="blast-sepolia-moonworm-crawler.service"
PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE="proofofplay-apex-moonworm-crawler.service"

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
echo -e "${PREFIX_INFO} Replacing existing Ethereum moonworm crawler service definition with ${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon moonworm crawler service definition with ${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Amoy moonworm crawler service definition with ${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing XDai moonworm crawler service definition with ${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era moonworm crawler service definition with ${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era Sepolia moonworm crawler service definition with ${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"


echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum One moonworm crawler service definition with ${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Nova moonworm crawler service definition with ${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Sepolia moonworm crawler service definition with ${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai moonworm crawler service definition with ${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia moonworm crawler service definition with ${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Avalanche moonworm crawler service definition with ${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Avalanche Fuji moonworm crawler service definition with ${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast moonworm crawler service definition with ${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast sepolia moonworm crawler service definition with ${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Proofofplay Apex moonworm crawler service definition with ${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"
