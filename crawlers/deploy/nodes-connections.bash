#!/usr/bin/env bash
#
# Update nodes connection address environment variables 
# from AWS Route53 internal hosted zone

VERSION='0.0.1'

# Colors
C_RESET='\033[0m'
C_RED='\033[1;31m'
C_GREEN='\033[1;32m'
C_YELLOW='\033[1;33m'

# Logs
PREFIX_INFO="${C_GREEN}[INFO]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_WARN="${C_YELLOW}[WARN]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_CRIT="${C_RED}[CRIT]${C_RESET} [$(date +%d-%m\ %T)]"

# Print help message
function usage {
  echo "Usage: $0 [-h] -p PRODUCT -f FILEPATH"  
  echo
  echo "CLI to update nodes connection address environment 
  variables from AWS Route53 internal hosted zone"
  echo
  echo "Optional arguments:"
  echo "  -h  Show this help message and exit"
  echo "  -f  File path where environment variables update at"
}

file_flag=""
verbose_flag="false"

while getopts 'f:v' flag; do
  case "${flag}" in
    f) file_flag="${OPTARG}" ;;
    h) usage
      exit 1 ;;
    v) verbose_flag="true" ;;
    *) usage
      exit 1 ;;
  esac
done

# Log messages
function verbose {
  if [ "${verbose_flag}" == "true" ]; then
    echo -e "$1"
  fi
}

# File flag should be specified
if [ -z "${file_flag}" ]; then
  verbose "${PREFIX_CRIT} Please specify file path"
  usage
  exit 1
fi

if [ ! -f "${file_flag}" ]; then
  verbose "${PREFIX_CRIT} Provided file does not exist"
  usage
  exit 1
fi

verbose "${PREFIX_INFO} Script version: v${VERSION}"

verbose "${PREFIX_INFO} Source environment variables"
. ${file_flag}

verbose "${PREFIX_INFO} Retrieving Ethereum node address"
RETRIEVED_NODE_ETHEREUM_IPC_ADDR=$(aws route53 list-resource-record-sets --hosted-zone-id "${MOONSTREAM_INTERNAL_HOSTED_ZONE_ID}" --query "ResourceRecordSets[?Name == '${MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI}.'].ResourceRecords[].Value" | jq -r .[0])
if [ "$RETRIEVED_NODE_ETHEREUM_IPC_ADDR" == "null" ]; then
  verbose "${PREFIX_CRIT} Ethereum node internal DNS record address is null"
  exit 1
fi

verbose "${PREFIX_INFO} Retrieving Polygon node address"
RETRIEVED_NODE_POLYGON_IPC_ADDR=$(aws route53 list-resource-record-sets --hosted-zone-id "${MOONSTREAM_INTERNAL_HOSTED_ZONE_ID}" --query "ResourceRecordSets[?Name == '${MOONSTREAM_POLYGON_WEB3_PROVIDER_URI}.'].ResourceRecords[].Value" | jq -r .[0])
if [ "$RETRIEVED_NODE_POLYGON_IPC_ADDR" == "null" ]; then
  verbose "${PREFIX_CRIT} Polygon node internal DNS record address is null"
  exit 1
fi

# TODO(kompotkot): Modify regexp to work with export prefix
verbose "${PREFIX_INFO} Updating MOONSTREAM_NODE_ETHEREUM_IPC_ADDR with ${RETRIEVED_NODE_ETHEREUM_IPC_ADDR}"
sed -i "s|^MOONSTREAM_NODE_ETHEREUM_IPC_ADDR=.*|MOONSTREAM_NODE_ETHEREUM_IPC_ADDR=\"$RETRIEVED_NODE_ETHEREUM_IPC_ADDR\"|" ${file_flag}

verbose "${PREFIX_INFO} Updating MOONSTREAM_NODE_POLYGON_IPC_ADDR with ${RETRIEVED_NODE_POLYGON_IPC_ADDR}"
sed -i "s|^MOONSTREAM_NODE_POLYGON_IPC_ADDR=.*|MOONSTREAM_NODE_POLYGON_IPC_ADDR=\"$RETRIEVED_NODE_POLYGON_IPC_ADDR\"|" ${file_flag}
