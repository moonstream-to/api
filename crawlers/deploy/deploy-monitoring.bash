#!/usr/bin/env bash

# Deployment script of monitoring services - intended to run on Moonstream crawlers server

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
PARAMETERS_ENV_MONITORING_PATH="${SECRETS_DIR}/monitoring.env"
SCRIPT_DIR="$(realpath $(dirname $0))"

# Service files
MONITORING_CRAWLERS_SERVICE_FILE="monitoring-crawlers.service"

set -eu

echo
echo
echo -e "${PREFIX_INFO} Install checkenv"
HOME=/home/ubuntu /usr/local/go/bin/go install github.com/bugout-dev/checkenv@latest

echo
echo
echo -e "${PREFIX_INFO} Copy monitoring binary from AWS S3"
aws s3 cp s3://bugout-binaries/prod/monitoring/monitoring "/home/ubuntu/monitoring"
chmod +x "/home/ubuntu/monitoring"
chown ubuntu:ubuntu "/home/ubuntu/monitoring"

echo
echo
echo -e "${PREFIX_INFO} Retrieving monitoring deployment parameters"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" /home/ubuntu/go/bin/checkenv show aws_ssm+crawlers:true,monitoring:true > "${PARAMETERS_ENV_MONITORING_PATH}"
chmod 0640 "${PARAMETERS_ENV_MONITORING_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Add instance local IP to monitoring parameters"
echo "AWS_LOCAL_IPV4=$(ec2metadata --local-ipv4)" >> "${PARAMETERS_ENV_MONITORING_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Add AWS default region to monitring parameters"
echo "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" >> "${PARAMETERS_ENV_MONITORING_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Prepare monitoring configuration"
if [ ! -d "/home/ubuntu/.monitoring" ]; then
  mkdir -p /home/ubuntu/.monitoring
  echo -e "${PREFIX_WARN} Created monitoring configuration directory"
fi
cp "${SCRIPT_DIR}/monitoring-crawlers-config.json" /home/ubuntu/.monitoring/monitoring-crawlers-config.json

echo
echo
if [ ! -d "/home/ubuntu/.config/systemd/user/" ]; then
  mkdir -p /home/ubuntu/.config/systemd/user/
  echo -e "${PREFIX_WARN} Created user systemd directory"
fi

echo
echo
echo -e "${PREFIX_INFO} Replacing existing systemd crawlers monitoring service definition with ${MONITORING_CRAWLERS_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${MONITORING_CRAWLERS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${MONITORING_CRAWLERS_SERVICE_FILE}" "/home/ubuntu/.config/systemd/user/${MONITORING_CRAWLERS_SERVICE_FILE}"
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user daemon-reload
XDG_RUNTIME_DIR="/run/user/1000" systemctl --user restart "${MONITORING_CRAWLERS_SERVICE_FILE}"
