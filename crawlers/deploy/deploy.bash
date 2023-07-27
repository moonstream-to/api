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
ETHEREUM_TRENDING_SERVICE_FILE="ethereum-trending.service"
ETHEREUM_TRENDING_TIMER_FILE="ethereum-trending.timer"
ETHEREUM_TXPOOL_SERVICE_FILE="ethereum-txpool.service"
ETHEREUM_MISSING_SERVICE_FILE="ethereum-missing.service"
ETHEREUM_MISSING_TIMER_FILE="ethereum-missing.timer"
ETHEREUM_MOONWORM_CRAWLER_SERVICE_FILE="ethereum-moonworm-crawler.service"
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
POLYGON_STATISTICS_SERVICE_FILE="polygon-statistics.service"
POLYGON_STATISTICS_TIMER_FILE="polygon-statistics.timer"
POLYGON_TXPOOL_SERVICE_FILE="polygon-txpool.service"
POLYGON_MOONWORM_CRAWLER_SERVICE_FILE="polygon-moonworm-crawler.service"
POLYGON_STATE_SERVICE_FILE="polygon-state.service"
POLYGON_STATE_TIMER_FILE="polygon-state.timer"
POLYGON_STATE_CLEAN_SERVICE_FILE="polygon-state-clean.service"
POLYGON_STATE_CLEAN_TIMER_FILE="polygon-state-clean.timer"
POLYGON_METADATA_SERVICE_FILE="polygon-metadata.service"
POLYGON_METADATA_TIMER_FILE="polygon-metadata.timer"
POLYGON_CU_REPORTS_TOKENONOMICS_SERVICE_FILE="polygon-cu-reports-tokenonomics.service"
POLYGON_CU_REPORTS_TOKENONOMICS_TIMER_FILE="polygon-cu-reports-tokenonomics.timer"
POLYGON_CU_NFT_DASHBOARD_SERVICE_FILE="polygon-cu-nft-dashboard.service"
POLYGON_CU_NFT_DASHBOARD_TIMER_FILE="polygon-cu-nft-dashboard.timer"
POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="polygon-historical-crawl-transactions.service"
POLYGON_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="polygon-historical-crawl-transactions.timer"
POLYGON_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="polygon-historical-crawl-events.service"
POLYGON_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="polygon-historical-crawl-events.timer"

# Mumbai service files
MUMBAI_SYNCHRONIZE_SERVICE="mumbai-synchronize.service"
MUMBAI_MISSING_SERVICE_FILE="mumbai-missing.service"
MUMBAI_MISSING_TIMER_FILE="mumbai-missing.timer"
MUMBAI_MOONWORM_CRAWLER_SERVICE_FILE="mumbai-moonworm-crawler.service"
MUMBAI_STATE_SERVICE_FILE="mumbai-state.service"
MUMBAI_STATE_TIMER_FILE="mumbai-state.timer"
MUMBAI_STATE_CLEAN_SERVICE_FILE="mumbai-state-clean.service"
MUMBAI_STATE_CLEAN_TIMER_FILE="mumbai-state-clean.timer"
MUMBAI_METADATA_SERVICE_FILE="mumbai-metadata.service"
MUMBAI_METADATA_TIMER_FILE="mumbai-metadata.timer"
MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="mumbai-historical-crawl-transactions.service"
MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="mumbai-historical-crawl-transactions.timer"
MUMBAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="mumbai-historical-crawl-events.service"
MUMBAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="mumbai-historical-crawl-events.timer"


# XDai service files
XDAI_SYNCHRONIZE_SERVICE="xdai-synchronize.service"
XDAI_MISSING_SERVICE_FILE="xdai-missing.service"
XDAI_MISSING_TIMER_FILE="xdai-missing.timer"
XDAI_STATISTICS_SERVICE_FILE="xdai-statistics.service"
XDAI_STATISTICS_TIMER_FILE="xdai-statistics.timer"
XDAI_MOONWORM_CRAWLER_SERVICE_FILE="xdai-moonworm-crawler.service"
XDai_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="xdai-historical-crawl-transactions.service"
XDai_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="xdai-historical-crawl-transactions.timer"
XDai_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="xdai-historical-crawl-events.service"
XDai_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="xdai-historical-crawl-events.timer"

# Wyrm service files
WYRM_SYNCHRONIZE_SERVICE="wyrm-synchronize.service"
WYRM_MISSING_SERVICE_FILE="wyrm-missing.service"
WYRM_MISSING_TIMER_FILE="wyrm-missing.timer"
WYRM_STATISTICS_SERVICE_FILE="wyrm-statistics.service"
WYRM_STATISTICS_TIMER_FILE="wyrm-statistics.timer"
WYRM_MOONWORM_CRAWLER_SERVICE_FILE="wyrm-moonworm-crawler.service"
WYRM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="wyrm-historical-crawl-transactions.service"
WYRM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="wyrm-historical-crawl-transactions.timer"
WYRM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="wyrm-historical-crawl-events.service"
WYRM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="wyrm-historical-crawl-events.timer"

# ZkSync Era testnet
ZKSYNC_ERA_TESTNET_SYNCHRONIZE_SERVICE="zksync-era-testnet-synchronize.service"
ZKSYNC_ERA_TESTNET_MISSING_SERVICE_FILE="zksync-era-testnet-missing.service"
ZKSYNC_ERA_TESTNET_MISSING_TIMER_FILE="zksync-era-testnet-missing.timer"
ZKSYNC_ERA_TESTNET_MOONWORM_CRAWLER_SERVICE_FILE="zksync-era-testnet-moonworm-crawler.service"
ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE="zksync-era-testnet-historical-crawl-transactions.service"
ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE="zksync-era-testnet-historical-crawl-transactions.timer"
ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE="zksync-era-testnet-historical-crawl-events.service"
ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_TIMER_FILE="zksync-era-testnet-historical-crawl-events.timer"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Building executable Ethereum transaction pool crawler script with Go"
EXEC_DIR=$(pwd)
cd "${APP_CRAWLERS_DIR}/txpool"
HOME=/home/ubuntu /usr/local/go/bin/go build -o "${APP_CRAWLERS_DIR}/txpool/txpool" "${APP_CRAWLERS_DIR}/txpool/main.go"
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
echo -e "${PREFIX_INFO} Install checkenv"
HOME=/home/ubuntu /usr/local/go/bin/go install github.com/bugout-dev/checkenv@latest

echo
echo
echo -e "${PREFIX_INFO} Retrieving addition deployment parameters"
mkdir -p "${SECRETS_DIR}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" /home/ubuntu/go/bin/checkenv show aws_ssm+moonstream:true > "${PARAMETERS_ENV_PATH}"
chmod 0640 "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Add instance local IP to parameters"
echo "AWS_LOCAL_IPV4=$(ec2metadata --local-ipv4)" >> "${PARAMETERS_ENV_PATH}"

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
echo -e "${PREFIX_INFO} Replacing existing Ethereum trending service and timer with: ${ETHEREUM_TRENDING_SERVICE_FILE}, ${ETHEREUM_TRENDING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_TRENDING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_TRENDING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_TRENDING_TIMER_FILE}"

# echo
# echo
# echo -e "${PREFIX_INFO} Replacing existing Ethereum transaction pool crawler service definition with ${ETHEREUM_TXPOOL_SERVICE_FILE}"
# chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE_FILE}"
# cp "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ETHEREUM_TXPOOL_SERVICE_FILE}"
# XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
# XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ETHEREUM_TXPOOL_SERVICE_FILE}"

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
echo -e "${PREFIX_INFO} Replacing existing Polygon statistics dashbord service and timer with: ${POLYGON_STATISTICS_SERVICE_FILE}, ${POLYGON_STATISTICS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_STATISTICS_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_STATISTICS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATISTICS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_STATISTICS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_STATISTICS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_STATISTICS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_STATISTICS_TIMER_FILE}"

# echo
# echo
# echo -e "${PREFIX_INFO} Replacing existing Polygon transaction pool crawler service definition with ${POLYGON_TXPOOL_SERVICE_FILE}"
# chmod 644 "${SCRIPT_DIR}/${POLYGON_TXPOOL_SERVICE_FILE}"
# cp "${SCRIPT_DIR}/${POLYGON_TXPOOL_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_TXPOOL_SERVICE_FILE}"
# XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
# XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_TXPOOL_SERVICE_FILE}"

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
echo -e "${PREFIX_INFO} Replacing existing Polygon CU reports tokenonomics service and timer with: ${POLYGON_CU_REPORTS_TOKENONOMICS_SERVICE_FILE}, ${POLYGON_CU_REPORTS_TOKENONOMICS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_CU_REPORTS_TOKENONOMICS_SERVICE_FILE}" "${SCRIPT_DIR}/${POLYGON_CU_REPORTS_TOKENONOMICS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_CU_REPORTS_TOKENONOMICS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_CU_REPORTS_TOKENONOMICS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${POLYGON_CU_REPORTS_TOKENONOMICS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${POLYGON_CU_REPORTS_TOKENONOMICS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${POLYGON_CU_REPORTS_TOKENONOMICS_TIMER_FILE}"

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

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Mumbai block with transactions syncronizer service definition with ${MUMBAI_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${MUMBAI_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MUMBAI_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Mumbai missing service and timer with: ${MUMBAI_MISSING_SERVICE_FILE}, ${MUMBAI_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${MUMBAI_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MUMBAI_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Mumbai moonworm crawler service definition with ${MUMBAI_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MUMBAI_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing MUMBAI state service and timer with: ${MUMBAI_STATE_SERVICE_FILE}, ${MUMBAI_STATE_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_STATE_SERVICE_FILE}" "${SCRIPT_DIR}/${MUMBAI_STATE_TIMER_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_STATE_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_STATE_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_STATE_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_STATE_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MUMBAI_STATE_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing MUMBAI state clean service and timer with: ${MUMBAI_STATE_CLEAN_SERVICE_FILE}, ${MUMBAI_STATE_CLEAN_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_STATE_CLEAN_SERVICE_FILE}" "${SCRIPT_DIR}/${MUMBAI_STATE_CLEAN_TIMER_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_STATE_CLEAN_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_STATE_CLEAN_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_STATE_CLEAN_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_STATE_CLEAN_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MUMBAI_STATE_CLEAN_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing MUMBAI metadata service and timer with: ${MUMBAI_METADATA_SERVICE_FILE}, ${MUMBAI_METADATA_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_METADATA_SERVICE_FILE}" "${SCRIPT_DIR}/${MUMBAI_METADATA_TIMER_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_METADATA_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_METADATA_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_METADATA_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_METADATA_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MUMBAI_METADATA_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing MUMBAI historical transactions crawler service and timer with: ${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MUMBAI_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing MUMBAI historical events crawler service and timer with: ${MUMBAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${MUMBAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MUMBAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${MUMBAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000"  systemctl --user restart --no-block "${MUMBAI_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

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
echo -e "${PREFIX_INFO} Replacing existing XDai statistics dashbord service and timer with: ${XDAI_STATISTICS_SERVICE_FILE}, ${XDAI_STATISTICS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${XDAI_STATISTICS_SERVICE_FILE}" "${SCRIPT_DIR}/${XDAI_STATISTICS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${XDAI_STATISTICS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${XDAI_STATISTICS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${XDAI_STATISTICS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${XDAI_STATISTICS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${XDAI_STATISTICS_TIMER_FILE}"

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

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Wyrm block with transactions syncronizer service definition with ${WYRM_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${WYRM_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${WYRM_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${WYRM_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${WYRM_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Wyrn missing service and timer with: ${WYRM_MISSING_SERVICE_FILE}, ${WYRM_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${WYRM_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${WYRM_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${WYRM_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${WYRM_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${WYRM_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Wyrm statistics dashbord service and timer with: ${WYRM_STATISTICS_SERVICE_FILE}, ${WYRM_STATISTICS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${WYRM_STATISTICS_SERVICE_FILE}" "${SCRIPT_DIR}/${WYRM_STATISTICS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${WYRM_STATISTICS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_STATISTICS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${WYRM_STATISTICS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_STATISTICS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${WYRM_STATISTICS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Wyrm moonworm crawler service definition with ${WYRM_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${WYRM_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${WYRM_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${WYRM_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Wyrm historical transactions crawler service and timer with: ${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${WYRM_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Wyrm historical events crawler service and timer with: ${WYRM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${WYRM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${WYRM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${WYRM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${WYRM_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"

# ZkSync Era
echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era testnet block with transactions syncronizer service definition with ${ZKSYNC_ERA_TESTNET_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_SYNCHRONIZE_SERVICE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_SYNCHRONIZE_SERVICE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_TESTNET_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era testnet missing service and timer with: ${ZKSYNC_ERA_TESTNET_MISSING_SERVICE_FILE}, ${ZKSYNC_ERA_TESTNET_MISSING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_MISSING_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_MISSING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_MISSING_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_MISSING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_MISSING_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_MISSING_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_TESTNET_MISSING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era testnet moonworm crawler service definition with ${ZKSYNC_ERA_TESTNET_MOONWORM_CRAWLER_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_MOONWORM_CRAWLER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_MOONWORM_CRAWLER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_MOONWORM_CRAWLER_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_TESTNET_MOONWORM_CRAWLER_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era testnet historical transactions crawler service and timer with: ${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}, ${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_TRANSACTIONS_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing ZkSync Era testnet historical events crawler service and timer with: ${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}, ${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${ZKSYNC_ERA_TESTNET_HISTORICAL_CRAWL_EVENTS_TIMER_FILE}"



echo
echo
echo -e "${PREFIX_INFO} Replacing existing Leaderboards worker service and timer with: ${LEADERBOARDS_WORKER_SERVICE_FILE}, ${LEADERBOARDS_WORKER_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_SERVICE_FILE}" "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_TIMER_FILE}"
cp "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${LEADERBOARDS_WORKER_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${LEADERBOARDS_WORKER_TIMER_FILE}" "/home/ubuntu/.config/systemd/user/${LEADERBOARDS_WORKER_TIMER_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${LEADERBOARDS_WORKER_TIMER_FILE}"