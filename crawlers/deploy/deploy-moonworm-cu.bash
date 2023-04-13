#!/usr/bin/env bash

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
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/moonworm-env}"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SCRIPT_DIR="$(realpath $(dirname $0))"

# Moonworm service files
MOONWORM_WATCH_UNICORNS_MAINNET_SERVICE_FILE="moonworm-unicorns-mainnet.service"

set -eu

if [ ! -d "$PYTHON_ENV_DIR" ]; then
  echo -e "${PREFIX_WARN} Dierectory with Python environment doesn't exist, generating..."
  python3.9 -m venv "${PYTHON_ENV_DIR}"
fi

echo
echo
echo -e "${PREFIX_INFO} Upgrading Python pip and setuptools"
"${PIP}" install --upgrade pip setuptools

echo
echo
echo -e "${PREFIX_INFO} Installing Python dependencies"
"${PIP}" install moonworm==0.2.4

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Moonworm watch Unicorns service definition with ${MOONWORM_WATCH_UNICORNS_MAINNET_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${MOONWORM_WATCH_UNICORNS_MAINNET_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MOONWORM_WATCH_UNICORNS_MAINNET_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MOONWORM_WATCH_UNICORNS_MAINNET_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart --no-block "${MOONWORM_WATCH_UNICORNS_MAINNET_SERVICE_FILE}"
