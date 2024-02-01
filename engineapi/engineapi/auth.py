"""
Login functionality for Moonstream Engine.

Login flow relies on an Authorization header passed to Moonstream Engine of the form:
Authorization: moonstream <base64-encoded JSON>

The schema for the JSON object will be as follows:
{
    "address": "<address of account which signed the message>",
    "deadline": <epoch timestamp after which this header becomes invalid>,
    "signature": "<signed authorization message>"
}

Authorization messages will be generated pursuant to EIP712 using the following parameters:
Domain separator - name: MoonstreamAuthorization, version: <Engine API version>
Fields - address ("address" type), deadline: ("uint256" type)
"""
import argparse
import base64
import json
import time
from typing import Any, Dict, Optional, cast

import eth_keys
from eip712.messages import EIP712Message, _hash_eip191_message
from eth_account import Account
from eth_account._utils.signing import sign_message_hash
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3


class MoonstreamAuthorizationVerificationError(Exception):
    """
    Raised when invalid signer is provided.
    """


class MoonstreamAuthorizationExpired(Exception):
    """
    Raised when signature is expired by time.
    """


class MoonstreamAuthorizationStructureError(Exception):
    """
    Raised when signature has incorrect structure.
    """


class MoonstreamAuthorization(EIP712Message):
    _name_: "string"  # type: ignore
    _version_: "string"  # type: ignore

    address: "address"  # type: ignore
    deadline: "uint256"  # type: ignore


class MetaTXAuthorization(EIP712Message):
    _name_: "string"  # type: ignore
    _version_: "string"  # type: ignore

    caller: "address"  # type: ignore
    expires_at: "uint256"  # type: ignore


EIP712_AUTHORIZATION_TYPES = {
    "MoonstreamAuthorization": {
        "name": "MoonstreamAuthorization",
        "version": "1",
        "eip712_message_class": MoonstreamAuthorization,
        "primary_types": [
            {"name": "address", "type": "address"},
            {"name": "deadline", "type": int},
        ],
    },
    "MetaTXAuthorization": {
        "name": "MetaTXAuthorization",
        "version": "1",
        "eip712_message_class": MetaTXAuthorization,
        "primary_types": [
            {"name": "caller", "type": "address"},
            {"name": "expires_at", "type": int},
        ],
    },
}


def sign_message(message_hash_bytes: HexBytes, private_key: HexBytes) -> HexBytes:
    eth_private_key = eth_keys.keys.PrivateKey(private_key)
    _, _, _, signed_message_bytes = sign_message_hash(
        eth_private_key, message_hash_bytes
    )
    return signed_message_bytes


def authorize(
    authorization_type: Dict[str, Any],
    primary_types: Dict[str, Any],
    private_key: HexBytes,
    signature_name_output: str,
) -> Dict[str, Any]:
    # Initializing instance of EIP712Message class
    attrs: Dict[str, Any] = {
        "_name_": authorization_type["name"],
        "_version_": authorization_type["version"],
    }
    attrs.update(primary_types)
    message = authorization_type["eip712_message_class"](**attrs)

    # Generating message hash and signature
    msg_hash_bytes = HexBytes(_hash_eip191_message(message.signable_message))

    signed_message = sign_message(msg_hash_bytes, private_key)

    api_payload: Dict[str, Any] = {signature_name_output: signed_message.hex()}
    api_payload.update(primary_types)

    return api_payload


def verify(
    authorization_type: Dict[str, Any],
    authorization_payload: Dict[str, Any],
    signature_name_input: str,
) -> bool:
    """
    Verifies provided signature signer by correct address.

    **Important** Assume that not address field is timefield (live_at, expires_at, deadline, etc)
    """
    # Initializing instance of EIP712Message class
    attrs: Dict[str, Any] = {
        "_name_": authorization_type["name"],
        "_version_": authorization_type["version"],
    }

    time_now = int(time.time())
    web3_client = Web3()

    address: Optional[ChecksumAddress] = None
    time_field: Optional[int] = None

    for pt in authorization_type["primary_types"]:
        pt_name = pt["name"]
        pt_type = pt["type"]
        if pt_type == "address":
            address = Web3.toChecksumAddress(cast(str, authorization_payload[pt_name]))
            attrs[pt_name] = address
        else:
            time_field = cast(pt_type, authorization_payload[pt_name])
            attrs[pt_name] = time_field
    if address is None or time_field is None:
        raise MoonstreamAuthorizationStructureError(
            "Field address or time_field could not be None"
        )

    message = authorization_type["eip712_message_class"](**attrs)
    signature = cast(str, authorization_payload[signature_name_input])
    signer_address = web3_client.eth.account.recover_message(
        message.signable_message, signature=signature
    )
    if signer_address != address:
        raise MoonstreamAuthorizationVerificationError("Invalid signer")

    if time_field < time_now:
        raise MoonstreamAuthorizationExpired("Time field exceeded")

    return True


def decrypt_keystore(keystore_path: str, password: str) -> HexBytes:
    with open(keystore_path) as keystore_file:
        keystore_data = json.load(keystore_file)
    return keystore_data["address"], Account.decrypt(keystore_data, password)


def handle_authorize(args: argparse.Namespace) -> None:
    if args.authorization_type not in EIP712_AUTHORIZATION_TYPES:
        raise Exception("Provided unsupported EIP712 Authorization type")

    authorization_type = EIP712_AUTHORIZATION_TYPES[args.authorization_type]
    primary_types = json.loads(args.primary_types)
    for ptk in authorization_type["primary_types"]:
        if ptk["name"] not in primary_types:
            raise Exception(f"Lost primary type: {ptk}")

    _, private_key = decrypt_keystore(args.signer, args.password)
    authorization = authorize(
        authorization_type=authorization_type,
        primary_types=primary_types,
        private_key=private_key,
        signature_name_output=args.signature_name_output,
    )
    print(json.dumps(authorization))


def handle_verify(args: argparse.Namespace) -> None:
    if args.authorization_type not in EIP712_AUTHORIZATION_TYPES:
        raise Exception("Provided unsupported EIP712 Authorization type")

    authorization_type = EIP712_AUTHORIZATION_TYPES[args.authorization_type]
    payload_json = base64.decodebytes(args.payload).decode("utf-8")
    payload = json.loads(payload_json)
    verify(
        authorization_type=authorization_type,
        authorization_payload=payload,
        signature_name_input=args.signature_name_input,
    )
    print("Verified!")


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Moonstream Engine authorization module"
    )
    subcommands = parser.add_subparsers()

    authorize_parser = subcommands.add_parser("authorize")
    authorize_parser.add_argument(
        "-s",
        "--signer",
        required=True,
        help="Path to signer keyfile (or brownie account name).",
    )
    authorize_parser.add_argument(
        "-p",
        "--password",
        required=False,
        help="(Optional) password for signing account. If you don't provide it here, you will be prompte for it.",
    )
    authorize_parser.add_argument(
        "-t",
        "--authorization-type",
        required=True,
        choices=[k for k in EIP712_AUTHORIZATION_TYPES.keys()],
        help="One of supported EIP712 Message authorization types",
    )
    authorize_parser.add_argument(
        "--primary-types",
        required=True,
        help="Primary types for specified EIP712 Message authorization in JSON format {0}. Available keys: {1}".format(
            {"name_1": "value", "name_2": "value"},
            [
                f"{v['primary_types']} for {k}"
                for k, v in EIP712_AUTHORIZATION_TYPES.items()
            ],
        ),
    )
    authorize_parser.add_argument(
        "--signature-name-output",
        type=str,
        default="signed_message",
        help="Key in output dictionary of signature",
    )
    authorize_parser.set_defaults(func=handle_authorize)

    verify_parser = subcommands.add_parser("verify")
    verify_parser.add_argument(
        "--payload",
        type=lambda s: s.encode(),
        required=True,
        help="Base64-encoded payload to verify",
    )
    verify_parser.add_argument(
        "-t",
        "--authorization-type",
        required=True,
        choices=[k for k in EIP712_AUTHORIZATION_TYPES.keys()],
        help="One of supported EIP712 Message authorization types",
    )
    verify_parser.add_argument(
        "--signature-name-input",
        type=str,
        default="signed_message",
        help="Key for signature in payload",
    )
    verify_parser.set_defaults(func=handle_verify)

    return parser


if __name__ == "__main__":
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)
