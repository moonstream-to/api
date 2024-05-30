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
ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE="ethereum-moonworm-crawler.service"
ETHEREUM_STATE_SERVICE_FILE="ethereum-state.service"
ETHEREUM_STATE_TIMER_FILE="ethereum-state.timer"
ETHEREUM_STATE_CLEAN_SERVICE_FILE="ethereum-state-clean.service"
ETHEREUM_STATE_CLEAN_TIMER_FILE="ethereum-state-clean.timer"
ETHEREUM_METADATA_SERVICE_FILE="ethereum-metadata.service"
ETHEREUM_METADATA_TIMER_FILE="ethereum-metadata.timer"
ETHEREUM_ORANGE_DAO_REPORTS_TOKENONOMICS_SERVICE_FILE="ethereum-orange-dao-reports-tokenonomics.service"
ETHEREUM_ORANGE_DAO_TOKENONOMICS_TIMER_FILE="ethereum-orange-dao-reports-tokenonomics.timer"
ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="ethereum-historical-crawl-transactions.service"
ETHEREUM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="ethereum-historical-crawl-transactions.timer"
ETHEREUM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="ethereum-historical-crawl-events.service"
ETHEREUM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="ethereum-historical-crawl-events.timer"

# Polygon service files
POLYGON_SYNCHRONIZE_SERVICE="polygon-synchronize.service"
POLYGON_MISSING_SERVICE_FILE="polygon-missing.service"
POLYGON_MISSING_TIMER_FILE="polygon-missing.timer"
POLYGON_MOONWORM_CRAWLER_SERVICE_FILE="polygon-moonworm-crawler.service"
POLYGON_STATE_SERVICE_FILE="polygon-state.service"
POLYGON_STATE_TIMER_FILE="polygon-state.timer"
POLYGON_STATE_CLEAN_SERVICE_FILE="polygon-state-clean.service"
POLYGON_STATE_CLEAN_TIMER_FILE="polygon-state-clean.timer"
POLYGON_METADATA_SERVICE_FILE="polygon-metadata.service"
POLYGON_METADATA_TIMER_FILE="polygon-metadata.timer"
POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE="polygon-cu-nft-dashboard.service"
POLYGON_CU_NFT_DASHBOARD_TIMER_FILE="polygon-cu-nft-dashboard.timer"
POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="polygon-historical-crawl-transactions.service"
POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="polygon-historical-crawl-transactions.timer"
POLYGON_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="polygon-historical-crawl-events.service"
POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="polygon-historical-crawl-events.timer"

# Amoy
AMOY_MISSING_SERVICE_FILE="amoy-missing.service"
AMOY_MISSING_TIMER_FILE="amoy-missing.timer"
AMOY_MOONWORM_CRAWLER_SERVICE_FILE="amoy-moonworm-crawler.service"
AMOY_SYNCHRONIZE_SERVICE="amoy-synchronize.service"
AMOY_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="amoy-historical-crawl-transactions.service"
AMOY_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="amoy-historical-crawl-transactions.timer"
AMOY_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="amoy-historical-crawl-events.service"
AMOY_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="amoy-historical-crawl-events.timer"

# XDai service files
XDAI_SYNCHRONIZE_SERVICE="xdai-synchronize.service"
XDAI_MISSING_SERVICE_FILE="xdai-missing.service"
XDAI_MISSING_TIMER_FILE="xdai-missing.timer"
XDAI_MOONWORM_CRAWLER_SERVICE_FILE="xdai-moonworm-crawler.service"
XDai_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="xdai-historical-crawl-transactions.service"
XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="xdai-historical-crawl-transactions.timer"
XDai_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="xdai-historical-crawl-events.service"
XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="xdai-historical-crawl-events.timer"

# ZkSync Era
ZKSYNC_ERA_SYNCHRONIZE_SERVICE="zksync-era-synchronize.service"
ZKSYNC_ERA_MISSING_SERVICE_FILE="zksync-era-missing.service"
ZKSYNC_ERA_MISSING_TIMER_FILE="zksync-era-missing.timer"
ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE="zksync-era-moonworm-crawler.service"
ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="zksync-era-historical-crawl-transactions.service"
ZKSYNC_ERA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="zksync-era-historical-crawl-transactions.timer"
ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="zksync-era-historical-crawl-events.service"
ZKSYNC_ERA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="zksync-era-historical-crawl-events.timer"
ZKSYNC_ERA_STATE_SERVICE_FILE="zksync-era-state.service"
ZKSYNC_ERA_STATE_TIMER_FILE="zksync-era-state.timer"
ZKSYNC_ERA_STATE_CLEAN_SERVICE_FILE="zksync-era-state-clean.service"
ZKSYNC_ERA_STATE_CLEAN_TIMER_FILE="zksync-era-state-clean.timer"

# ZkSync Era Sepolia
ZKSYNC_ERA_SEPOLIA_SYNCHRONIZE_SERVICE="zksync-era-sepolia-synchronize.service"
ZKSYNC_ERA_SEPOLIA_MISSING_SERVICE_FILE="zksync-era-sepolia-missing.service"
ZKSYNC_ERA_SEPOLIA_MISSING_TIMER_FILE="zksync-era-sepolia-missing.timer"
ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="zksync-era-sepolia-moonworm-crawler.service"
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="zksync-era-sepolia-historical-crawl-transactions.service"
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="zksync-era-sepolia-historical-crawl-transactions.timer"
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="zksync-era-sepolia-historical-crawl-events.service"
ZKSYNC_ERA_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="zksync-era-sepolia-historical-crawl-events.timer"

# Arbitrum Nova
ARBITRUM_NOVA_MISSING_SERVICE_FILE="arbitrum-nova-missing.service"
ARBITRUM_NOVA_MISSING_TIMER_FILE="arbitrum-nova-missing.timer"
ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE="arbitrum-nova-moonworm-crawler.service"
ARBITRUM_NOVA_SYNCHRONIZE_SERVICE="arbitrum-nova-synchronize.service"

# Arbitrum one
ARBITRUM_ONE_SYNCHRONIZE_SERVICE="arbitrum-one-synchronize.service"
ARBITRUM_ONE_MISSING_SERVICE_FILE="arbitrum-one-missing.service"
ARBITRUM_ONE_MISSING_TIMER_FILE="arbitrum-one-missing.timer"
ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE="arbitrum-one-moonworm-crawler.service"
ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="arbitrum-one-historical-crawl-transactions.service"
ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="arbitrum-one-historical-crawl-transactions.timer"
ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="arbitrum-one-historical-crawl-events.service"
ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="arbitrum-one-historical-crawl-events.timer"

# Arbitrum Sepolia
ARBITRUM_SEPOLIA_MISSING_SERVICE_FILE="arbitrum-sepolia-missing.service"
ARBITRUM_SEPOLIA_MISSING_TIMER_FILE="arbitrum-sepolia-missing.timer"
ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="arbitrum-sepolia-moonworm-crawler.service"
ARBITRUM_SEPOLIA_SYNCHRONIZE_SERVICE="arbitrum-sepolia-synchronize.service"

# Xai
XAI_MISSING_SERVICE_FILE="xai-missing.service"
XAI_MISSING_TIMER_FILE="xai-missing.timer"
XAI_MOONWORM_CRAWLER_SERVICE_FILE="xai-moonworm-crawler.service"
XAI_SYNCHRONIZE_SERVICE="xai-synchronize.service"
XAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="xai-historical-crawl-events.service"
XAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="xai-historical-crawl-events.timer"
XAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="xai-historical-crawl-transactions.service"
XAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="xai-historical-crawl-transactions.timer"


# Xai sepolia
XAI_SEPOLIA_MISSING_SERVICE_FILE="xai-sepolia-missing.service"
XAI_SEPOLIA_MISSING_TIMER_FILE="xai-sepolia-missing.timer"
XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="xai-sepolia-moonworm-crawler.service"
XAI_SEPOLIA_SYNCHRONIZE_SERVICE="xai-sepolia-synchronize.service"
XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="xai-sepolia-historical-crawl-events.service"
XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="xai-sepolia-historical-crawl-events.timer"
XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="xai-sepolia-historical-crawl-transactions.service"
XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="xai-sepolia-historical-crawl-transactions.timer"

# Avalanche
AVALANCHE_SYNCHRONIZE_SERVICE="avalanche-synchronize.service"
AVALANCHE_MISSING_SERVICE_FILE="avalanche-missing.service"
AVALANCHE_MISSING_TIMER_FILE="avalanche-missing.timer"
AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE="avalanche-moonworm-crawler.service"

# Avalanche Fuji
AVALANCHE_FUJI_SYNCHRONIZE_SERVICE="avalanche-fuji-synchronize.service"
AVALANCHE_FUJI_MISSING_SERVICE_FILE="avalanche-fuji-missing.service"
AVALANCHE_FUJI_MISSING_TIMER_FILE="avalanche-fuji-missing.timer"
AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE="avalanche-fuji-moonworm-crawler.service"

# Blast
BLAST_MISSING_SERVICE_FILE="blast-missing.service"
BLAST_MISSING_TIMER_FILE="blast-missing.timer"
BLAST_MOONWORM_CRAWLER_SERVICE_FILE="blast-moonworm-crawler.service"
BLAST_SYNCHRONIZE_SERVICE="blast-synchronize.service"

# Blast sepolia
BLAST_SEPOLIA_MISSING_SERVICE_FILE="blast-sepolia-missing.service"
BLAST_SEPOLIA_MISSING_TIMER_FILE="blast-sepolia-missing.timer"
BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE="blast-sepolia-moonworm-crawler.service"
BLAST_SEPOLIA_SYNCHRONIZE_SERVICE="blast-sepolia-synchronize.service"

# ProofofPlay APEX
PROOFOFPLAY_APEX_MISSING_SERVICE_FILE="proofofplay-apex-missing.service"
PROOFOFPLAY_APEX_MISSING_TIMER_FILE="proofofplay-apex-missing.timer"
PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE="proofofplay-apex-moonworm-crawler.service"
PROOFOFPLAY_APEX_SYNCHRONIZE_SERVICE="proofofplay-apex-synchronize.service"
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
echo -e "${PREFIX_INFO} Replacing existing Moonstream crawlers HTTP API server service definition with ${MOONCRAWL_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${MOONCRAWL_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MOONCRAWL_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MOONCRAWL_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MOONCRAWL_SERVICE_FILE}"

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
echo -e "${PREFIX_INFO} Replacing existing Ethereum moonworm crawler service definition with ${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE}"

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
echo -e "${PREFIX_INFO} Replacing existing Polygon moonworm crawler service definition with ${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_MOONWORM_CRAWLER_SERVICE_FILE}"

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
echo -e "${PREFIX_INFO} Replacing existing Polygon CU reports tokenonomics service and timer with: ${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}, ${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_CU_NFT_DASHBOARD_TIMER_FILE}"

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

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Amoy moonworm crawler service definition with ${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AMOY_MOONWORM_CRAWLER_SERVICE_FILE}"

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
echo -e "${PREFIX_INFO} Replacing existing XDai moonworm crawler service definition with ${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XDAI_MOONWORM_CRAWLER_SERVICE_FILE}"

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

# ZkSync Era
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
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era moonworm crawler service definition with ${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_MOONWORM_CRAWLER_SERVICE_FILE}"

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

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Leaderboards worker service and timer with: ${LEADERBOARDS_WORKER_SERVICE_FILE}, ${LEADERBOARDS_WORKER_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_SERVICE_FILE}" "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_TIMER_FILE}"
cp "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${LEADERBOARDS_WORKER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${LEADERBOARDS_WORKER_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${LEADERBOARDS_WORKER_TIMER_FILE}"

# ZkSync Era Sepolia
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
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era Sepolia moonworm crawler service definition with ${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"

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

# Arbitrum Nova
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
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Nova moonworm crawler service definition with ${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_NOVA_MOONWORM_CRAWLER_SERVICE_FILE}"

# Arbitrum one
echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum one block with transactions syncronizer service definition with ${ARBITRUM_ONE_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_ONE_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_ONE_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum one missing service and timer with: ${ARBITRUM_ONE_MISSING_SERVICE_FILE}, ${ARBITRUM_ONE_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_ONE_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ARBITRUM_ONE_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_ONE_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum One moonworm crawler service definition with ${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_ONE_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum one historical transactions crawler service and timer with: ${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_ONE_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Arbitrum one historical events crawler service and timer with: ${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_ONE_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"


# Arbitrum Sepolia
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
echo -e "${PREFIX_INFO} Replacing existing Arbitrum Sepolia moonworm crawler service definition with ${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ARBITRUM_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"

# Xai
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
echo -e "${PREFIX_INFO} Replacing existing Xai moonworm crawler service definition with ${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai historical transactions crawler service and timer with: ${XAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${XAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai historical events crawler service and timer with: ${XAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${XAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000"  systemctl --user restart --no-block "${XAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"



# Xai sepolia
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
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia moonworm crawler service definition with ${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia historical transactions crawler service and timer with: ${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XAI_SEPOLIA_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Xai sepolia historical events crawler service and timer with: ${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000"  systemctl --user restart --no-block "${XAI_SEPOLIA_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

# Avalanche
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
echo -e "${PREFIX_INFO} Replacing existing Avalanche moonworm crawler service definition with ${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_MOONWORM_CRAWLER_SERVICE_FILE}"

# Avalanche Fuji
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

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Avalanche Fuji moonworm crawler service definition with ${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${AVALANCHE_FUJI_MOONWORM_CRAWLER_SERVICE_FILE}"

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

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast moonworm crawler service definition with ${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_MOONWORM_CRAWLER_SERVICE_FILE}"

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

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Blast sepolia moonworm crawler service definition with ${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${BLAST_SEPOLIA_MOONWORM_CRAWLER_SERVICE_FILE}"


# Proofofplay Apex

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Proofofplay Apex block with transactions syncronizer service definition with ${PROOFOFPLAY_APEX_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${PROOFOFPLAY_APEX_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Proofofplay Apex missing service and timer with: ${PROOFOFPLAY_APEX_MISSING_SERVICE_FILE}, ${PROOFOFPLAY_APEX_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${PROOFOFPLAY_APEX_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Proofofplay Apex moonworm crawler service definition with ${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${PROOFOFPLAY_APEX_MOONWORM_CRAWLER_SERVICE_FILE}"

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
