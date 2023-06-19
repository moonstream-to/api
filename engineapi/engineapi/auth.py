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
from typing import Any, cast, Dict

from eip712.messages import EIP712Message, _hash_eip191_message
from eth_account import Account
from eth_account._utils.signing import sign_message_hash
import eth_keys
from hexbytes import HexBytes
from web3 import Web3


AUTH_PAYLOAD_NAME = "MoonstreamAuthorization"
AUTH_VERSION = "1"

# By default, authorizations will remain active for 24 hours.
DEFAULT_INTERVAL = 60 * 60 * 24


class MoonstreamAuthorizationVerificationError(Exception):
    """
    Raised when invalid signer is provided.
    """


class MoonstreamAuthorizationExpired(Exception):
    """
    Raised when signature is expired by time.
    """


class MoonstreamAuthorization(EIP712Message):
    _name_: "string"
    _version_: "string"

    address: "address"
    deadline: "uint256"


def sign_message(message_hash_bytes: HexBytes, private_key: HexBytes) -> HexBytes:
    eth_private_key = eth_keys.keys.PrivateKey(private_key)
    _, _, _, signed_message_bytes = sign_message_hash(
        eth_private_key, message_hash_bytes
    )
    return signed_message_bytes


def authorize(deadline: int, address: str, private_key: HexBytes) -> Dict[str, Any]:
    message = MoonstreamAuthorization(
        _name_=AUTH_PAYLOAD_NAME,
        _version_=AUTH_VERSION,
        address=address,
        deadline=deadline,
    )

    msg_hash_bytes = HexBytes(_hash_eip191_message(message.signable_message))

    signed_message = sign_message(msg_hash_bytes, private_key)

    api_payload: Dict[str, Any] = {
        "address": address,
        "deadline": deadline,
        "signed_message": signed_message.hex(),
    }

    return api_payload


def verify(authorization_payload: Dict[str, Any]) -> bool:
    """
    Verifies provided signature signer by correct address.
    """
    time_now = int(time.time())
    web3_client = Web3()
    address = Web3.toChecksumAddress(cast(str, authorization_payload["address"]))
    deadline = cast(int, authorization_payload["deadline"])
    signature = cast(str, authorization_payload["signed_message"])

    message = MoonstreamAuthorization(
        _name_=AUTH_PAYLOAD_NAME,
        _version_=AUTH_VERSION,
        address=address,
        deadline=deadline,
    )

    signer_address = web3_client.eth.account.recover_message(
        message.signable_message, signature=signature
    )
    if signer_address != address:
        raise MoonstreamAuthorizationVerificationError("Invalid signer")

    if deadline < time_now:
        raise MoonstreamAuthorizationExpired("Deadline exceeded")

    return True


def decrypt_keystore(keystore_path: str, password: str) -> HexBytes:
    with open(keystore_path) as keystore_file:
        keystore_data = json.load(keystore_file)
    return keystore_data["address"], Account.decrypt(keystore_data, password)


def handle_authorize(args: argparse.Namespace) -> None:
    address, private_key = decrypt_keystore(args.signer, args.password)
    authorization = authorize(args.deadline, address, private_key)
    print(json.dumps(authorization))


def handle_verify(args: argparse.Namespace) -> None:
    payload_json = base64.decodebytes(args.payload).decode("utf-8")
    payload = json.loads(payload_json)
    verify(payload)
    print("Verified!")


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Moonstream Engine authorization module"
    )
    subcommands = parser.add_subparsers()

    authorize_parser = subcommands.add_parser("authorize")
    authorize_parser.add_argument(
        "-t",
        "--deadline",
        type=int,
        default=int(time.time()) + DEFAULT_INTERVAL,
        help="Authorization deadline (seconds since epoch timestamp).",
    )
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
    authorize_parser.set_defaults(func=handle_authorize)

    verify_parser = subcommands.add_parser("verify")
    verify_parser.add_argument(
        "--payload",
        type=lambda s: s.encode(),
        required=True,
        help="Base64-encoded payload to verify",
    )
    verify_parser.set_defaults(func=handle_verify)

    return parser


if __name__ == "__main__":
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)
