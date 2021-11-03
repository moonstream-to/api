#!/usr/bin/env bash
#
# Collect secrets from AWS SSM Parameter Store and output as environment variable exports.

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
  echo "Usage: $0 [-h] -p PRODUCT -o OUTPUT"  
  echo
  echo "CLI to collect secrets from AWS SSM Parameter Store 
and output as environment variable exports"
  echo
  echo "Optional arguments:"
  echo "  -h  Show this help message and exit"
  echo "  -p  Product tag (moonstream, spire, brood, drones)"
  echo "  -o  Output file name environment variables export to"
}

product_flag=""
output_flag=""
verbose_flag="false"

while getopts 'p:o:v' flag; do
  case "${flag}" in
    p) product_flag="${OPTARG}" ;;
    o) output_flag="${OPTARG}" ;;
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

# Product flag should be specified
# TODO(kompotkot): Extend script to work with few product at once
if [ -z "${product_flag}" ]; then
  verbose "${PREFIX_CRIT} Please specify product tag"
  usage
  exit 1
fi

verbose "${PREFIX_INFO} Retrieving deployment parameters with tag ${C_GREEN}Product:${product_flag}${C_RESET}"
ENV_PARAMETERS=$(aws ssm describe-parameters \
  --parameter-filters Key=tag:Product,Values=${product_flag} \
  | jq -r .Parameters[].Name)
if [ -z "${ENV_PARAMETERS}" ]; then
  verbose "${PREFIX_CRIT} There no parameters for provided product tag"
  exit 1
fi

verbose "${PREFIX_INFO} Retrieving parameters values"
ENV_PARAMETERS_VALUES=$(aws ssm get-parameters \
  --names ${ENV_PARAMETERS} \
  --query "Parameters[*].{Name:Name,Value:Value}")
ENV_PARAMETERS_VALUES_LENGTH=$(echo ${ENV_PARAMETERS_VALUES} | jq length)
verbose "${PREFIX_INFO} Extracted ${ENV_PARAMETERS_VALUES_LENGTH} parameters"
for i in $(seq 0 $((${ENV_PARAMETERS_VALUES_LENGTH} - 1))); do
  param_key=$(echo ${ENV_PARAMETERS_VALUES} | jq -r .[$i].Name)
  param_value=$(echo ${ENV_PARAMETERS_VALUES} | jq .[$i].Value)
  if [ -z "${output_flag}" ]; then
    echo "${param_key}=${param_value}"
  else
    echo "${param_key}=${param_value}" >> "${output_flag}"
  fi
done
