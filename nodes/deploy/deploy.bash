#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream node control server

# Main
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
NODE_PARAMETERS_ENV_PATH="${SECRETS_DIR}/node.env"
SCRIPT_DIR="$(realpath $(dirname $0))"
ETHEREUM_GETH_SERVICE="ethereum-node.service"

set -eu

echo
echo
echo "Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
> "${NODE_PARAMETERS_ENV_PATH}"
ENV_PARAMETERS=$(aws ssm describe-parameters \
    --parameter-filters Key=tag:Product,Values=moonstream Key=tag:Blockchain,Values=ethereum \
    | jq -r .Parameters[].Name)
ENV_PARAMETERS_VALUES=$(aws ssm get-parameters \
    --names $ENV_PARAMETERS \
    --query "Parameters[*].{Name:Name,Value:Value}")
ENV_PARAMETERS_VALUES_LENGTH=$(($(echo $ENV_PARAMETERS_VALUES | jq length) - 1))
for i in $(seq 0 $ENV_PARAMETERS_VALUES_LENGTH)
do
    param_key=$(echo $ENV_PARAMETERS_VALUES | jq -r .[$i].Name)
    if [ "$param_key" == "MOONSTREAM_NODE_ETHEREUM_IPC_ADDR" ]
    then
        LOCAL_IP="$(curl http://169.254.169.254/latest/meta-data/local-ipv4)"
        param_value="\"$LOCAL_IP\""
    else
        param_value=$(echo $ENV_PARAMETERS_VALUES | jq .[$i].Value)
    fi
    echo "export $param_key=$param_value" >> "${NODE_PARAMETERS_ENV_PATH}"
done

echo
echo
echo "Replacing Ethereum Geth service definition with ${ETHEREUM_GETH_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_GETH_SERVICE}"
cp "${SCRIPT_DIR}/${ETHEREUM_GETH_SERVICE}" "/etc/systemd/system/${ETHEREUM_GETH_SERVICE}"
systemctl daemon-reload
systemctl disable "${ETHEREUM_GETH_SERVICE}"

if systemctl is-active --quiet "${ETHEREUM_GETH_SERVICE}"
then
    echo "Ethereum Geth service ${ETHEREUM_GETH_SERVICE} already running"
else
    echo "Restart Geth service ${ETHEREUM_GETH_SERVICE}"
    systemctl restart "${ETHEREUM_GETH_SERVICE}"
    sleep 10
fi
