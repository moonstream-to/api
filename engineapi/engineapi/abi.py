"""
ABI utilities, because web3 doesn't do selectors well.
"""

import glob
import json
import os
from typing import Any, Dict, List, Optional

from web3 import Web3


def abi_input_signature(input_abi: Dict[str, Any]) -> str:
    """
    Stringifies a function ABI input object according to the ABI specification:
    https://docs.soliditylang.org/en/v0.5.3/abi-spec.html
    """
    input_type = input_abi["type"]
    if input_type.startswith("tuple"):
        component_types = [
            abi_input_signature(component) for component in input_abi["components"]
        ]
        input_type = f"({','.join(component_types)}){input_type[len('tuple'):]}"
    return input_type


def abi_function_signature(function_abi: Dict[str, Any]) -> str:
    """
    Stringifies a function ABI according to the ABI specification:
    https://docs.soliditylang.org/en/v0.5.3/abi-spec.html
    """
    function_name = function_abi["name"]
    function_arg_types = [
        abi_input_signature(input_item) for input_item in function_abi["inputs"]
    ]
    function_signature = f"{function_name}({','.join(function_arg_types)})"
    return function_signature


def encode_function_signature(function_abi: Dict[str, Any]) -> Optional[str]:
    """
    Encodes the given function (from ABI) with arguments arg_1, ..., arg_n into its 4 byte signature
    by calculating:
    keccak256("<function_name>(<arg_1_type>,...,<arg_n_type>")

    If function_abi is not actually a function ABI (detected by checking if function_abi["type"] == "function),
    returns None.
    """
    if function_abi["type"] != "function":
        return None
    function_signature = abi_function_signature(function_abi)
    encoded_signature = Web3.keccak(text=function_signature)[:4]
    return encoded_signature.hex()


def project_abis(project_dir: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Load all ABIs for project contracts and return then in a dictionary keyed by contract name.

    Inputs:
    - project_dir
      Path to brownie project
    """
    build_dir = os.path.join(project_dir, "build", "contracts")
    build_files = glob.glob(os.path.join(build_dir, "*.json"))

    abis: Dict[str, List[Dict[str, Any]]] = {}

    for filepath in build_files:
        contract_name, _ = os.path.splitext(os.path.basename(filepath))
        with open(filepath, "r") as ifp:
            contract_artifact = json.load(ifp)

        contract_abi = contract_artifact.get("abi", [])

        abis[contract_name] = contract_abi

    return abis
