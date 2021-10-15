#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream node control server

# Main
SCRIPT_DIR="$(realpath $(dirname $0))"
ETHEREUM_GETH_SERVICE="ethereum-node.service"

set -eu

echo
echo
echo "Deploy Geth service if not running already"
if systemctl is-active --quiet "${ETHEREUM_GETH_SERVICE}"
then
    echo "Ethereum Geth service ${ETHEREUM_GETH_SERVICE} already running"
else
    echo "Replacing Ethereum Geth service definition with ${ETHEREUM_GETH_SERVICE}"
    chmod 644 "${SCRIPT_DIR}/${ETHEREUM_GETH_SERVICE}"
    cp "${SCRIPT_DIR}/${ETHEREUM_GETH_SERVICE}" "/etc/systemd/system/${ETHEREUM_GETH_SERVICE}"
    systemctl daemon-reload
    systemctl disable "${ETHEREUM_GETH_SERVICE}"
    systemctl restart "${ETHEREUM_GETH_SERVICE}"
    sleep 10
fi
