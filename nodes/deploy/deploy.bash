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
BLOCKCHAIN="ethereum"
ETHEREUM_GETH_SERVICE="ethereum-node.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
> "${NODE_PARAMETERS_ENV_PATH}"

LOCAL_IP="$(curl http://169.254.169.254/latest/meta-data/local-ipv4)"
echo -e "${PREFIX_INFO} Found assign subnet IP ${C_GREEN}${LOCAL_IP}${C_RESET} for machine"
ENV_PARAMETERS=$(aws ssm describe-parameters \
    --parameter-filters Key=tag:Product,Values=moonstream Key=tag:Blockchain,Values=$BLOCKCHAIN \
    | jq -r .Parameters[].Name)
ENV_PARAMETERS_VALUES=$(aws ssm get-parameters \
    --names $ENV_PARAMETERS \
    --query "Parameters[*].{Name:Name,Value:Value}")
ENV_PARAMETERS_VALUES_LENGTH=$(echo $ENV_PARAMETERS_VALUES | jq length)
echo -e "${PREFIX_INFO} Extracted ${ENV_PARAMETERS_VALUES_LENGTH} parameters"
for i in $(seq 0 $(($ENV_PARAMETERS_VALUES_LENGTH - 1)))
do
    param_key=$(echo $ENV_PARAMETERS_VALUES | jq -r .[$i].Name)
    if [ "$param_key" == "MOONSTREAM_NODE_ETHEREUM_IPC_ADDR" ] && [ -n "$LOCAL_IP" ] 
    then
        param_value="\"$LOCAL_IP\""
    else
        param_value=$(echo $ENV_PARAMETERS_VALUES | jq .[$i].Value)
    fi
    echo "export $param_key=$param_value" >> "${NODE_PARAMETERS_ENV_PATH}"
done

echo
echo
echo "${PREFIX_INFO} Replacing Ethereum Geth service definition with ${ETHEREUM_GETH_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_GETH_SERVICE}"
cp "${SCRIPT_DIR}/${ETHEREUM_GETH_SERVICE}" "/etc/systemd/system/${ETHEREUM_GETH_SERVICE}"
systemctl daemon-reload
systemctl disable "${ETHEREUM_GETH_SERVICE}"

if systemctl is-active --quiet "${ETHEREUM_GETH_SERVICE}"
then
    echo "${PREFIX_WARN} Ethereum Geth service ${ETHEREUM_GETH_SERVICE} already running"
else
    echo "${PREFIX_INFO} Restart Geth service ${ETHEREUM_GETH_SERVICE}"
    systemctl restart "${ETHEREUM_GETH_SERVICE}"
    sleep 10
fi
