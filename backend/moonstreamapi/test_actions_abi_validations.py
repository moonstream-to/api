import unittest

from .actions import dashboards_abi_validation
from .data import DashboardMeta
from .middleware import MoonstreamHTTPException

abi_example = [
    {
        "inputs": [
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "string", "name": "_symbol", "type": "string"},
            {"internalType": "string", "name": "_uri", "type": "string"},
            {"internalType": "address", "name": "owner", "type": "address"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "operator",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "approved",
                "type": "bool",
            },
        ],
        "name": "ApprovalForAll",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnershipTransferred",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "operator",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "ids",
                "type": "uint256[]",
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "values",
                "type": "uint256[]",
            },
        ],
        "name": "TransferBatch",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "operator",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "TransferSingle",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "value",
                "type": "string",
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256",
            },
        ],
        "name": "URI",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "id", "type": "uint256"},
        ],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address[]", "name": "accounts", "type": "address[]"},
            {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
        ],
        "name": "balanceOfBatch",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_account", "type": "address"},
            {"internalType": "uint256[]", "name": "_ids", "type": "uint256[]"},
            {"internalType": "uint256", "name": "_amaunt", "type": "uint256"},
            {"internalType": "bytes[]", "name": "_data", "type": "bytes[]"},
        ],
        "name": "batchMint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_cid", "type": "string"},
            {"internalType": "bytes", "name": "_data", "type": "bytes"},
        ],
        "name": "create",
        "outputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "address", "name": "operator", "type": "address"},
        ],
        "name": "isApprovedForAll",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_account", "type": "address"},
            {"internalType": "uint256", "name": "_id", "type": "uint256"},
            {"internalType": "uint256", "name": "_amaunt", "type": "uint256"},
            {"internalType": "bytes", "name": "_data", "type": "bytes"},
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "pause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "paused",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"},
            {"internalType": "bytes", "name": "data", "type": "bytes"},
        ],
        "name": "safeBatchTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "bytes", "name": "data", "type": "bytes"},
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "operator", "type": "address"},
            {"internalType": "bool", "name": "approved", "type": "bool"},
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}],
        "name": "supportsInterface",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
        "name": "uri",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]


subscription = {
    "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
    "generic": [
        {"name": "transactions_in"},
        {"name": "transactions_out"},
        {"name": "value_in"},
        {"name": "value_out"},
        {"name": "balance"},
    ],
    "methods": [
        {"name": "transferOwnership", "filters": {"newOwner": "110392"}}
    ],  # incorrect but valid because address represent just string for validator
    "events": [{"name": "OwnershipTransferred"}, {"name": 0}],
}


class TestValidateStreamBoundary(unittest.TestCase):
    def test_valid_functions_and_event_subscription(self):

        subscription = DashboardMeta(
            **{
                "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
                "generic": [
                    {"name": "transactions_in"},
                    {"name": "transactions_out"},
                    {"name": "value_in"},
                    {"name": "value_out"},
                    {"name": "balance"},
                ],
                "methods": [
                    {"name": "transferOwnership", "filters": {"newOwner": "110392"}}
                ],  # incorrect but valid because address represent just string for validator
                "events": [
                    {"name": "OwnershipTransferred", "filters": {"newOwner": "110392"}}
                ],
            }
        )

        print(dashboards_abi_validation(subscription, abi_example, s3_path=""))

        self.assertEqual(
            dashboards_abi_validation(subscription, abi_example, s3_path=""),
            True,
        )

    def test_invalid_function_name_subscription(self):
        subscription = DashboardMeta(
            **{
                "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
                "generic": [
                    {"name": "transactions_in"},
                    {"name": "transactions_out"},
                    {"name": "value_in"},
                    {"name": "value_out"},
                    {"name": "balance"},
                ],
                "methods": [
                    {
                        "name": "transferBlockchainOwnership",
                        "filters": {"newOwner": "110392"},
                    }
                ],  # incorrect but valid because address represent just string for validator
                "events": [
                    {"name": "OwnershipTransferred", "filters": {"newOwner": "110392"}}
                ],
            }
        )

        with self.assertRaises(MoonstreamHTTPException):

            dashboards_abi_validation(subscription, abi_example, s3_path="")

    def test_invalid_function_arg_name_subscription(self):
        subscription = DashboardMeta(
            **{
                "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
                "generic": [
                    {"name": "transactions_in"},
                    {"name": "transactions_out"},
                    {"name": "value_in"},
                    {"name": "value_out"},
                    {"name": "balance"},
                ],
                "methods": [
                    {
                        "name": "transferOwnership",
                        "filters": {"newOwners": "110392"},
                    }
                ],  # incorrect but valid because address represent just string for validator
                "events": [
                    {"name": "OwnershipTransferred", "filters": {"newOwner": "110392"}}
                ],
            }
        )

        with self.assertRaises(MoonstreamHTTPException):

            dashboards_abi_validation(subscription, abi_example, s3_path="")

    def test_invalid_function_arg_type_subscription(self):
        subscription = DashboardMeta(
            **{
                "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
                "generic": [
                    {"name": "transactions_in"},
                    {"name": "transactions_out"},
                    {"name": "value_in"},
                    {"name": "value_out"},
                    {"name": "balance"},
                ],
                "methods": [
                    {
                        "name": "transferOwnership",
                        "filters": {"newOwner": 110392},
                    }
                ],  # incorrect but valid because address represent just string for validator
                "events": [
                    {"name": "OwnershipTransferred", "filters": {"newOwner": "110392"}}
                ],
            }
        )

        with self.assertRaises(MoonstreamHTTPException):

            dashboards_abi_validation(subscription, abi_example, s3_path="")

    def test_invalid_event_name_subscription(self):
        subscription = DashboardMeta(
            **{
                "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
                "generic": [
                    {"name": "transactions_in"},
                    {"name": "transactions_out"},
                    {"name": "value_in"},
                    {"name": "value_out"},
                    {"name": "balance"},
                ],
                "methods": [
                    {"name": "transferOwnership", "filters": {"newOwner": "110392"}}
                ],
                "events": [
                    {"name": "OwnershipDisappeared", "filters": {"newOwner": "110392"}}
                ],
            }
        )
        with self.assertRaises(MoonstreamHTTPException):

            dashboards_abi_validation(subscription, abi_example, s3_path="")

    def test_invalid_event_arg_name_subscription(self):
        subscription = DashboardMeta(
            **{
                "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
                "generic": [
                    {"name": "transactions_in"},
                    {"name": "transactions_out"},
                    {"name": "value_in"},
                    {"name": "value_out"},
                    {"name": "balance"},
                ],
                "methods": [
                    {"name": "transferOwnership", "filters": {"newOwner": "110392"}}
                ],
                "events": [
                    {
                        "name": "OwnershipTransferred",
                        "filters": {"blockchainOwner": "110392"},
                    }
                ],
            }
        )

        with self.assertRaises(MoonstreamHTTPException):

            dashboards_abi_validation(subscription, abi_example, s3_path="")

    def test_invalid_event_arg_type_subscription(self):
        subscription = DashboardMeta(
            **{
                "subscription_id": "0869942d-3cd2-4ea5-9424-d0f3e1653173",
                "generic": [
                    {"name": "transactions_in"},
                    {"name": "transactions_out"},
                    {"name": "value_in"},
                    {"name": "value_out"},
                    {"name": "balance"},
                ],
                "methods": [
                    {"name": "transferOwnership", "filters": {"newOwner": "110392"}}
                ],
                "events": [
                    {"name": "OwnershipTransferred", "filters": {"newOwner": True}}
                ],
            }
        )

        with self.assertRaises(MoonstreamHTTPException):

            dashboards_abi_validation(subscription, abi_example, s3_path="")


if __name__ == "__main__":
    unittest.main()
