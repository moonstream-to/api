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
MOONCRAWL_SERVICE_FILE="mooncrawl.service"
LEADERBOARDS_WORKER_SERVICE_FILE="leaderboards-worker.service"
LEADERBOARDS_WORKER_TIMER_FILE="leaderboards-worker.timer"

# Ethereum service files
ETHEREUM_SYNCHRONIZE_SERVICE_FILE="ethereum-synchronize.service"
ETHEREUM_MISSING_SERVICE_FILE="ethereum-missing.service"
ETHEREUM_MISSING_TIMER_FILE="ethereum-missing.timer"
ETHEREUM_ORANGE_DAO_REPORTS_TOKENONOMICS_SERVICE_FILE="ethereum-orange-dao-reports-tokenonomics.service"
ETHEREUM_ORANGE_DAO_TOKENONOMICS_TIMER_FILE="ethereum-orange-dao-reports-tokenonomics.timer"

# Polygon service files
POLYGON_SYNCHRONIZE_SERVICE="polygon-synchronize.service"
POLYGON_MISSING_SERVICE_FILE="polygon-missing.service"
POLYGON_MISSING_TIMER_FILE="polygon-missing.timer"
POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE="polygon-cu-nft-dashboard.service"
POLYGON_CU_NFT_DASHBOARD_TIMER_FILE="polygon-cu-nft-dashboard.timer"

# Mumbai service files
MUMBAI_SYNCHRONIZE_SERVICE="mumbai-synchronize.service"
MUMBAI_MISSING_SERVICE_FILE="mumbai-missing.service"
MUMBAI_MISSING_TIMER_FILE="mumbai-missing.timer"

# Amoy
AMOY_MISSING_SERVICE_FILE="amoy-missing.service"
AMOY_MISSING_TIMER_FILE="amoy-missing.timer"
AMOY_SYNCHRONIZE_SERVICE="amoy-synchronize.service"

# XDai service files
XDAI_SYNCHRONIZE_SERVICE="xdai-synchronize.service"
XDAI_MISSING_SERVICE_FILE="xdai-missing.service"
XDAI_MISSING_TIMER_FILE="xdai-missing.timer"

# ZkSync Era
ZKSYNC_ERA_SYNCHRONIZE_SERVICE="zksync-era-synchronize.service"
ZKSYNC_ERA_MISSING_SERVICE_FILE="zksync-era-missing.service"
ZKSYNC_ERA_MISSING_TIMER_FILE="zksync-era-missing.timer"

# ZkSync Era Sepolia
ZKSYNC_ERA_SEPOLIA_SYNCHRONIZE_SERVICE="zksync-era-sepolia-synchronize.service"
ZKSYNC_ERA_SEPOLIA_MISSING_SERVICE_FILE="zksync-era-sepolia-missing.service"
ZKSYNC_ERA_SEPOLIA_MISSING_TIMER_FILE="zksync-era-sepolia-missing.timer"

# Arbitrum Nova
ARBITRUM_NOVA_SYNCHRONIZE_SERVICE="arbitrum-nova-synchronize.service"
ARBITRUM_NOVA_MISSING_SERVICE_FILE="arbitrum-nova-missing.service"
ARBITRUM_NOVA_MISSING_TIMER_FILE="arbitrum-nova-missing.timer"

# Arbitrum Sepolia
ARBITRUM_SEPOLIA_SYNCHRONIZE_SERVICE="arbitrum-sepolia-synchronize.service"
ARBITRUM_SEPOLIA_MISSING_SERVICE_FILE="arbitrum-sepolia-missing.service"
ARBITRUM_SEPOLIA_MISSING_TIMER_FILE="arbitrum-sepolia-missing.timer"

# Xai
XAI_SYNCHRONIZE_SERVICE="xai-synchronize.service"
XAI_MISSING_SERVICE_FILE="xai-missing.service"
XAI_MISSING_TIMER_FILE="xai-missing.timer"

# Xai sepolia
XAI_SEPOLIA_SYNCHRONIZE_SERVICE="xai-sepolia-synchronize.service"
XAI_SEPOLIA_MISSING_SERVICE_FILE="xai-sepolia-missing.service"
XAI_SEPOLIA_MISSING_TIMER_FILE="xai-sepolia-missing.timer"

# Avalanche sepolia
AVALANCHE_SYNCHRONIZE_SERVICE="avalanche-synchronize.service"
AVALANCHE_MISSING_SERVICE_FILE="avalanche-missing.service"
AVALANCHE_MISSING_TIMER_FILE="avalanche-missing.timer"

# Avalanche Fuji sepolia
AVALANCHE_FUJI_SYNCHRONIZE_SERVICE="avalanche-fuji-synchronize.service"
AVALANCHE_FUJI_MISSING_SERVICE_FILE="avalanche-fuji-missing.service"
AVALANCHE_FUJI_MISSING_TIMER_FILE="avalanche-fuji-missing.timer"

# Blast
BLAST_MISSING_SERVICE_FILE="blast-missing.service"
BLAST_MISSING_TIMER_FILE="blast-missing.timer"
BLAST_SYNCHRONIZE_SERVICE="blast-synchronize.service"

# Blast sepolia
BLAST_SEPOLIA_MISSING_SERVICE_FILE="blast-sepolia-missing.service"
BLAST_SEPOLIA_MISSING_TIMER_FILE="blast-sepolia-missing.timer"
BLAST_SEPOLIA_SYNCHRONIZE_SERVICE="blast-sepolia-synchronize.service"

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
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" /home/ubuntu/go/bin/checkenv show aws_ssm+moonstream:true > "${PARAMETERS_ENV_PATH}"
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
echo -e "${PREFIX_INFO} Replacing existing Moonstream crawlers HTTP API server service definition with ${MOONCRAWL_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${MOONCRAWL_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MOONCRAWL_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MOONCRAWL_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MOONCRAWL_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Leaderboards worker service and timer with: ${LEADERBOARDS_WORKER_SERVICE_FILE}, ${LEADERBOARDS_WORKER_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_SERVICE_FILE}" "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_TIMER_FILE}"
cp "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${LEADERBOARDS_WORKER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${LEADERBOARDS_WORKER_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${LEADERBOARDS_WORKER_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum block with transactions syncronizer service definition with ${ETHEREUM_SYNCHRONIZE_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_SYNCHRONIZE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_SYNCHRONIZE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_SYNCHRONIZE_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_SYNCHRONIZE_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum missing service and timer with: ${ETHEREUM_MISSING_SERVICE_FILE}, ${ETHEREUM_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum Orange DAO reports tokenonomics service and timer with: ${ETHEREUM_ORANGE_DAO_REPORTS_TOKENONOMICS_SERVICE_FILE}, ${ETHEREUM_ORANGE_DAO_TOKENONOMICS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_ORANGE_DAO_REPORTS_TOKENONOMICS_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_ORANGE_DAO_TOKENONOMICS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_ORANGE_DAO_REPORTS_TOKENONOMICS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_ORANGE_DAO_REPORTS_TOKENONOMICS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_ORANGE_DAO_TOKENONOMICS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_ORANGE_DAO_TOKENONOMICS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_ORANGE_DAO_TOKENONOMICS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon block with transactions syncronizer service definition with ${POLYGON_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${POLYGON_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${POLYGON_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon missing service and timer with: ${POLYGON_MISSING_SERVICE_FILE}, ${POLYGON_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon CU reports tokenonomics service and timer with: ${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}, ${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"

# Amoy
echo
echo
echo -e "${PREFIX_INFO} Replacing existing Amoy block with transactions syncronizer service definition with ${AMOY_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${AMOY_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${AMOY_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${AMOY_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AMOY_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Amoy missing service and timer with: ${AMOY_MISSING_SERVICE_FILE}, ${AMOY_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${AMOY_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${AMOY_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${AMOY_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AMOY_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AMOY_MISSING_TIMER_FILE}"

# Xdai
echo
echo
echo -e "${PREFIX_INFO} Replacing existing XDai block with transactions syncronizer service definition with ${XDAI_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${XDAI_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${XDAI_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${XDAI_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XDAI_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing XDai missing service and timer with: ${XDAI_MISSING_SERVICE_FILE}, ${XDAI_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XDAI_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${XDAI_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XDAI_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XDAI_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XDAI_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XDAI_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XDAI_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era block with transactions syncronizer service definition with ${ZKSYNC_ERA_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era missing service and timer with: ${ZKSYNC_ERA_MISSING_SERVICE_FILE}, ${ZKSYNC_ERA_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era Sepolia block with transactions syncronizer service definition with ${ZKSYNC_ERA_SEPOLIA_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_SEPOLIA_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era Sepolia missing service and timer with: ${ZKSYNC_ERA_SEPOLIA_MISSING_SERVICE_FILE}, ${ZKSYNC_ERA_SEPOLIA_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_SEPOLIA_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Nova block with transactions syncronizer service definition with ${ARBITRUM_NOVA_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_NOVA_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ARBITRUM_NOVA_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_NOVA_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_NOVA_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Nova missing service and timer with: ${ARBITRUM_NOVA_MISSING_SERVICE_FILE}, ${ARBITRUM_NOVA_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_NOVA_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ARBITRUM_NOVA_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_NOVA_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_NOVA_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_NOVA_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_NOVA_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_NOVA_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Sepolia block with transactions syncronizer service definition with ${ARBITRUM_SEPOLIA_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_SEPOLIA_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_SEPOLIA_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Sepolia missing service and timer with: ${ARBITRUM_SEPOLIA_MISSING_SERVICE_FILE}, ${ARBITRUM_SEPOLIA_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_SEPOLIA_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_SEPOLIA_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_SEPOLIA_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai block with transactions syncronizer service definition with ${XAI_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${XAI_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${XAI_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai missing service and timer with: ${XAI_MISSING_SERVICE_FILE}, ${XAI_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia block with transactions syncronizer service definition with ${XAI_SEPOLIA_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia missing service and timer with: ${XAI_SEPOLIA_MISSING_SERVICE_FILE}, ${XAI_SEPOLIA_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_SEPOLIA_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Avalanche block with transactions syncronizer service definition with ${AVALANCHE_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${AVALANCHE_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Avalanche missing service and timer with: ${AVALANCHE_MISSING_SERVICE_FILE}, ${AVALANCHE_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${AVALANCHE_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Avalanche Fuji block with transactions syncronizer service definition with ${AVALANCHE_FUJI_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_FUJI_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${AVALANCHE_FUJI_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_FUJI_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_FUJI_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Avalanche Fuji missing service and timer with: ${AVALANCHE_FUJI_MISSING_SERVICE_FILE}, ${AVALANCHE_FUJI_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_FUJI_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${AVALANCHE_FUJI_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_FUJI_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_FUJI_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_FUJI_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_FUJI_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_FUJI_MISSING_TIMER_FILE}"

# Blast
echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast block with transactions syncronizer service definition with ${BLAST_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${BLAST_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${BLAST_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast missing service and timer with: ${BLAST_MISSING_SERVICE_FILE}, ${BLAST_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${BLAST_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${BLAST_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${BLAST_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_MISSING_TIMER_FILE}"

# Blast sepolia
echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast sepolia block with transactions syncronizer service definition with ${BLAST_SEPOLIA_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_SEPOLIA_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${BLAST_SEPOLIA_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${BLAST_SEPOLIA_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_SEPOLIA_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast sepolia missing service and timer with: ${BLAST_SEPOLIA_MISSING_SERVICE_FILE}, ${BLAST_SEPOLIA_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_SEPOLIA_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${BLAST_SEPOLIA_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${BLAST_SEPOLIA_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_SEPOLIA_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${BLAST_SEPOLIA_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_SEPOLIA_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_SEPOLIA_MISSING_TIMER_FILE}"
