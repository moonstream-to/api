#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream Polygon node control server

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
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"
SCRIPT_DIR="$(realpath $(dirname $0))"
BLOCKCHAIN="polygon"
HEIMDALL_HOME="/mnt/disks/nodes/${BLOCKCHAIN}/.heimdalld"

# Parameters scripts
CHECKENV_PARAMETERS_SCRIPT="${SCRIPT_DIR}/parameters.bash"
CHECKENV_NODES_CONNECTIONS_SCRIPT="${SCRIPT_DIR}/nodes-connections.bash"

# Polygon heimdalld service files
POLYGON_HEIMDALLD_SERVICE_FILE="heimdalld.service"
POLYGON_HEIMDALLD_BRIDGE_SERVICE_FILE="heimdalld-bridge.service"
POLYGON_HEIMDALLD_REST_SERVICE_FILE="heimdalld-rest-server.service"

# Polygon bor service file
POLYGON_BOR_SERVICE_FILE="bor.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
> "${PARAMETERS_ENV_PATH}"
bash "${CHECKENV_PARAMETERS_SCRIPT}" -vn -p "moonstream" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Updating nodes connection parameters"
bash "${CHECKENV_NODES_CONNECTIONS_SCRIPT}" -v -f "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Replacing current node IP environment variable with local IP"
LOCAL_IP="$(ec2metadata --local-ipv4)"
sed -i "s|MOONSTREAM_NODE_POLYGON_IPC_ADDR=.*|MOONSTREAM_NODE_POLYGON_IPC_ADDR=\"$LOCAL_IP\"|" "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Source extracted parameters"
. "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Update heimdall config file with Ethereum URI"
MOONSTREAM_NODE_ETHEREUM_IPC_URI="http://$MOONSTREAM_NODE_ETHEREUM_IPC_ADDR:$MOONSTREAM_NODE_ETHEREUM_IPC_PORT"
sed -i "s|^eth_rpc_url =.*|eth_rpc_url = \"$MOONSTREAM_NODE_ETHEREUM_IPC_URI\"|" "${HEIMDALL_HOME}/config/heimdall-config.toml"
echo -e "${PREFIX_INFO} Updated ${C_GREEN}eth_rpc_url = $MOONSTREAM_NODE_ETHEREUM_IPC_URI${C_RESET} for heimdall"
