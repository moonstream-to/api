"""
Signing and signature verification functionality and interfaces.
"""
import abc
import logging
import json
from typing import Any, List, Optional, Union

import boto3
from web3 import Web3

from eth_account import Account
from eth_account.messages import encode_defunct
from eth_account._utils.signing import sign_message_hash
import eth_keys
import requests
from hexbytes import HexBytes

from .settings import (
    SIGNER_KEYSTORE,
    SIGNER_PASSWORD,
    MOONSTREAM_SIGNING_SERVER_IP,
    AWS_DEFAULT_REGION,
    MOONSTREAM_AWS_SIGNER_LAUNCH_TEMPLATE_ID,
    MOONSTREAM_AWS_SIGNER_IMAGE_ID,
    MOONSTREAM_AWS_SIGNER_INSTANCE_PORT,
)

logger = logging.getLogger(__name__)

aws_client = boto3.client("ec2", region_name=AWS_DEFAULT_REGION)


class AWSDescribeInstancesFail(Exception):
    """
    Raised when AWS describe instances command failed.
    """


class AWSRunInstancesFail(Exception):
    """
    Raised when AWS run instances command failed.
    """


class AWSTerminateInstancesFail(Exception):
    """
    Raised when AWS terminate instances command failed.
    """


class SigningInstancesNotFound(Exception):
    """
    Raised when signing instances with the given ids is not found in at AWS.
    """


class SigningInstancesTerminationLimitExceeded(Exception):
    """
    Raised when provided several instances to termination.
    """


class SignWithInstanceFail(Exception):
    """
    Raised when failed signing of message with instance server.
    """


class Signer:
    @abc.abstractmethod
    def sign_message(self, message):
        pass

    @abc.abstractmethod
    def refresh_signer(self):
        pass

    @abc.abstractmethod
    def batch_sign_message(self, messages_list):
        pass


class AccountSigner(Signer):
    """
    Simple implementation of a signer that uses a Brownie account to sign messages.
    """

    def __init__(self, private_key: HexBytes) -> None:
        self.private_key = private_key

    def sign_message(self, message):
        eth_private_key = eth_keys.keys.PrivateKey(self.private_key)
        message_hash_bytes = HexBytes(message)
        _, _, _, signed_message_bytes = sign_message_hash(
            eth_private_key, message_hash_bytes
        )
        return signed_message_bytes.hex()

    def batch_sign_message(self, messages_list: List[str]):
        signed_messages_list = {}

        for message in messages_list:
            eth_private_key = eth_keys.keys.PrivateKey(self.private_key)
            message_hash_bytes = HexBytes(message)
            _, _, _, signed_message_bytes = sign_message_hash(
                eth_private_key, message_hash_bytes
            )
            signed_messages_list[message.hex()] = signed_message_bytes.hex()

        return signed_messages_list


def create_account_signer(keystore: str, password: str) -> AccountSigner:
    with open(keystore) as keystore_file:
        keystore_data = json.load(keystore_file)
    private_key = Account.decrypt(keystore_data, password)
    signer = AccountSigner(private_key)
    return signer


class InstanceSigner(Signer):
    """
    AWS instance server signer.
    """

    def __init__(self, ip: Optional[str] = None) -> None:
        self.current_signer_uri = None
        if ip is not None:
            self.current_signer_uri = (
                f"http://{ip}:{MOONSTREAM_AWS_SIGNER_INSTANCE_PORT}/sign"
            )
            self.current_signer_batch_uri = (
                f"http://{ip}:{MOONSTREAM_AWS_SIGNER_INSTANCE_PORT}/batchsign"
            )

    def clean_signer(self) -> None:
        self.current_signer_uri = None
        self.current_signer_batch_uri = None

    def refresh_signer(self) -> None:
        try:
            instances = list_signing_instances([])
        except AWSDescribeInstancesFail:
            raise AWSDescribeInstancesFail("AWS describe instances command failed")
        except Exception as err:
            logger.error(f"AWS describe instances command failed: {err}")
            raise SignWithInstanceFail("AWS describe instances command failed")

        if len(instances) != 1:
            raise SignWithInstanceFail("Unsupported number of signing instances")

        self.current_signer_uri = f"http://{instances[0]['private_ip_address']}:{MOONSTREAM_AWS_SIGNER_INSTANCE_PORT}/sign"
        self.current_signer_batch_uri = f"http://{instances[0]['private_ip_address']}:{MOONSTREAM_AWS_SIGNER_INSTANCE_PORT}/batchsign"

    def sign_message(self, message: str):
        # TODO(kompotkot): What to do if self.current_signer_uri is not None but the signing server went down?
        if self.current_signer_uri is None:
            self.refresh_signer()

        signed_message = ""
        try:
            resp = requests.post(
                self.current_signer_uri,
                headers={"Content-Type": "application/json"},
                json={"unsigned_data": str(message)},
            )
            resp.raise_for_status()
            body = resp.json()
            signed_message = body["signed_data"]
        except Exception as err:
            logger.error(f"Failed signing of message with instance server, {err}")
            raise SignWithInstanceFail("Failed signing of message with instance server")

        # Hack as per: https://medium.com/@yaoshiang/ethereums-ecrecover-openzeppelin-s-ecdsa-and-web3-s-sign-8ff8d16595e1
        signature = signed_message[2:]
        if signature[-2:] == "00":
            signature = f"{signature[:-2]}1b"
        elif signature[-2:] == "01":
            signature = f"{signature[:-2]}1c"
        else:
            raise SignWithInstanceFail(
                f"Unexpected v-value on signed message: {signed_message[-2:]}"
            )

        return signature

    def batch_sign_message(self, messages_list: List[str]):
        if self.current_signer_uri is None:
            self.refresh_signer()

        try:
            resp = requests.post(
                self.current_signer_batch_uri,
                headers={"Content-Type": "application/json"},
                json={"unsigned_data": [str(message) for message in messages_list]},
            )
            resp.raise_for_status()
            signed_messages = resp.json()["signed_data"]
        except Exception as err:
            logger.error(f"Failed signing of message with instance server, {err}")
            raise SignWithInstanceFail("Failed signing of message with instance server")

        results = {}

        # Hack as per: https://medium.com/@yaoshiang/ethereums-ecrecover-openzeppelin-s-ecdsa-and-web3-s-sign-8ff8d16595e1
        for unsigned_message, signed_message in signed_messages.items():
            signature = signed_message[2:]
            if signature[-2:] == "00":
                signature = f"{signature[:-2]}1b"
            elif signature[-2:] == "01":
                signature = f"{signature[:-2]}1c"
            else:
                raise SignWithInstanceFail(
                    f"Unexpected v-value on signed message: {signed_message[-2:]}"
                )
            results[unsigned_message] = signature

        return results


DROP_SIGNER: Optional[Signer] = None
if SIGNER_KEYSTORE is not None and SIGNER_PASSWORD is not None:
    DROP_SIGNER = create_account_signer(SIGNER_KEYSTORE, SIGNER_PASSWORD)
if DROP_SIGNER is None:
    DROP_SIGNER = InstanceSigner(MOONSTREAM_SIGNING_SERVER_IP)


def list_signing_instances(
    signing_instances: List[str],
) -> List[Any]:
    """
    Return a list of signing instances with IPs.
    """
    described_instances = []
    try:
        described_instances_response = aws_client.describe_instances(
            Filters=[
                {"Name": "image-id", "Values": [MOONSTREAM_AWS_SIGNER_IMAGE_ID]},
                {"Name": "tag:Application", "Values": ["signer"]},
            ],
            InstanceIds=signing_instances,
        )
        for r in described_instances_response["Reservations"]:
            for i in r["Instances"]:
                described_instances.append(
                    {
                        "instance_id": i["InstanceId"],
                        "private_ip_address": i["PrivateIpAddress"],
                    }
                )
    except Exception as err:
        logger.error(f"AWS describe instances command failed: {err}")
        raise AWSDescribeInstancesFail("AWS describe instances command failed.")

    return described_instances


def wakeup_signing_instances(run_confirmed=False, dry_run=True) -> List[str]:
    """
    Run new signing instances.
    """
    run_instances = []
    if run_confirmed:
        try:
            run_instances_response = aws_client.run_instances(
                LaunchTemplate={
                    "LaunchTemplateId": MOONSTREAM_AWS_SIGNER_LAUNCH_TEMPLATE_ID
                },
                MinCount=1,
                MaxCount=1,
                DryRun=dry_run,
            )
            for i in run_instances_response["Instances"]:
                run_instances.append(i["InstanceId"])
        except Exception as err:
            logger.error(f"AWS run instances command failed: {err}")
            raise AWSRunInstancesFail("AWS run instances command failed")

    return run_instances


def sleep_signing_instances(
    signing_instances: List[str], termination_confirmed=False, dry_run=True
) -> List[str]:
    """
    Fetch, describe, verify signing instances and terminate them.
    """
    if len(signing_instances) == 0:
        raise SigningInstancesNotFound("There are no signing instances to describe")

    described_instances = []
    try:
        described_instances_response = list_signing_instances(signing_instances)
        for i in described_instances_response:
            described_instances.append(i["instance_id"])
    except Exception as err:
        logger.error(f"AWS describe instances command failed: {err}")
        raise AWSDescribeInstancesFail("AWS describe instances command failed.")

    if len(described_instances) == 0:
        raise SigningInstancesNotFound(
            "Signing instances with the given ids is not found in at AWS."
        )
    if len(described_instances) > 1:
        raise SigningInstancesTerminationLimitExceeded(
            f"Provided {len(described_instances)} instances to termination"
        )

    terminated_instances = []
    if termination_confirmed:
        try:
            terminated_instances_response = aws_client.terminate_instances(
                InstanceIds=described_instances,
                DryRun=dry_run,
            )
            for i in terminated_instances_response["TerminatingInstances"]:
                terminated_instances.append(i["InstanceId"])
        except Exception as err:
            logger.error(
                f"Unable to terminate instance {described_instances}, error: {err}"
            )
            raise AWSTerminateInstancesFail("AWS terminate instances command failed")

    return terminated_instances
