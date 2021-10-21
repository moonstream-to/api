#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream node control server
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
NODE_PARAMETERS_ENV_PATH="${SECRETS_DIR}/node.env"
SCRIPT_DIR="$(realpath $(dirname $0))"
BLOCKCHAIN="polygon"
HEIMDALL_HOME="/mnt/disks/nodes/${BLOCKCHAIN}"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
> "${NODE_PARAMETERS_ENV_PATH}"

GETH_NODE_ADDR=$(dig +short ethereum.moonstream.internal)
GETH_NODE_PORT=$(aws ssm get-parameters --names MOONSTREAM_NODE_ETHEREUM_IPC_PORT --query "Parameters[*]" | jq -r .[0].Value)
if [ -n "$GETH_NODE_ADDR" ] && [ -n "$GETH_NODE_PORT" ]
then
    MOONSTREAM_NODE_ETHEREUM_IPC_URI="http://$GETH_NODE_ADDR:$GETH_NODE_PORT"
    echo "MOONSTREAM_NODE_ETHEREUM_IPC_URI=\"$MOONSTREAM_NODE_ETHEREUM_IPC_URI\"" >> "${NODE_PARAMETERS_ENV_PATH}"
    sed -i "s|^eth_rpc_url =.*|eth_rpc_url = \"$MOONSTREAM_NODE_ETHEREUM_IPC_URI\"|" $HEIMDALL_HOME/config/heimdall-config.toml
    echo -e "${PREFIX_INFO} Updated ${C_GREEN}eth_rpc_url = $MOONSTREAM_NODE_ETHEREUM_IPC_URI${C_RESET} for Heimdall"
fi
