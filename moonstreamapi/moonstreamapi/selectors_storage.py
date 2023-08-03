from typing import Any, Dict

selectors: Dict[str, Any] = {
    "274c7b3c": {
        "name": "ERC20PresetMinterPauser",
        "selector": "274c7b3c",
        "abi": [
            {
                "inputs": [],
                "name": "DEFAULT_ADMIN_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "MINTER_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "PAUSER_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burnFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"}
                ],
                "name": "getRoleAdmin",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "getRoleMember",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"}
                ],
                "name": "getRoleMemberCount",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "grantRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "hasRole",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "renounceRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "revokeRole",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "unpause",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DEFAULT_ADMIN_ROLE",
            "MINTER_ROLE",
            "PAUSER_ROLE",
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "burnFrom",
            "decimals",
            "decreaseAllowance",
            "getRoleAdmin",
            "getRoleMember",
            "getRoleMemberCount",
            "grantRole",
            "hasRole",
            "increaseAllowance",
            "mint",
            "name",
            "pause",
            "paused",
            "renounceRole",
            "revokeRole",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
            "unpause",
        ],
    },
    "a264d2b1": {
        "name": "ERC777Mock",
        "selector": "a264d2b1",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "holder", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "holder", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "approveInternal",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "authorizeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "tokenHolder",
                        "type": "address",
                    }
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "pure",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "defaultOperators",
                "outputs": [
                    {"internalType": "address[]", "name": "", "type": "address[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "granularity",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "tokenHolder",
                        "type": "address",
                    },
                ],
                "name": "isOperatorFor",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "mintInternal",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                    {
                        "internalType": "bool",
                        "name": "requireReceptionAck",
                        "type": "bool",
                    },
                ],
                "name": "mintInternalExtended",
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
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorBurn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorSend",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "revokeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "send",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "holder", "type": "address"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "approveInternal",
            "authorizeOperator",
            "balanceOf",
            "burn",
            "decimals",
            "defaultOperators",
            "granularity",
            "isOperatorFor",
            "mintInternal",
            "mintInternalExtended",
            "name",
            "operatorBurn",
            "operatorSend",
            "revokeOperator",
            "send",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "01ffc9a7": {
        "name": "ERC165MaliciousData",
        "selector": "01ffc9a7",
        "abi": [
            {
                "inputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "pure",
                "type": "function",
            }
        ],
        "functions_names": ["supportsInterface"],
    },
    "572b6c05": {
        "name": "ERC2771Context",
        "selector": "572b6c05",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "forwarder", "type": "address"}
                ],
                "name": "isTrustedForwarder",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["isTrustedForwarder"],
    },
    "8ef63f04": {
        "name": "ERC4626LimitsMock",
        "selector": "8ef63f04",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxDeposit",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxRedeem",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxWithdraw",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {"inputs": [], "name": "MathOverflowedMulDiv", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "SafeERC20FailedOperation",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Deposit",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Withdraw",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "decreaseAllowance",
            "deposit",
            "increaseAllowance",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "36372b07": {
        "name": "IERC20",
        "selector": "36372b07",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "8ba81481": {
        "name": "ERC1155Pausable",
        "selector": "8ba81481",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC1155InsufficientApprovalForAll",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC1155InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC1155InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "idsLength", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "valuesLength",
                        "type": "uint256",
                    },
                ],
                "name": "ERC1155InvalidArrayLength",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC1155InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC1155InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC1155InvalidSender",
                "type": "error",
            },
            {"inputs": [], "name": "EnforcedPause", "type": "error"},
            {"inputs": [], "name": "ExpectedPause", "type": "error"},
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
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Paused",
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
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Unpaused",
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
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
                "inputs": [],
                "name": "paused",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "isApprovedForAll",
            "paused",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "uri",
        ],
    },
    "bf86c12d": {
        "name": "ERC721BurnableMock",
        "selector": "bf86c12d",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "exists",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "bytes", "name": "_data", "type": "bytes"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "burn",
            "exists",
            "getApproved",
            "isApprovedForAll",
            "mint",
            "name",
            "ownerOf",
            "safeMint",
            "safeMint",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "2fec9aa3": {
        "name": "ERC20VotesComp",
        "selector": "2fec9aa3",
        "abi": [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint32", "name": "pos", "type": "uint32"},
                ],
                "name": "checkpoints",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "fromBlock",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint224",
                                "name": "votes",
                                "type": "uint224",
                            },
                        ],
                        "internalType": "struct ERC20Votes.Checkpoint",
                        "name": "",
                        "type": "tuple",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getCurrentVotes",
                "outputs": [{"internalType": "uint96", "name": "", "type": "uint96"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    }
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "name": "getPriorVotes",
                "outputs": [{"internalType": "uint96", "name": "", "type": "uint96"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "numCheckpoints",
                "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "allowance",
            "approve",
            "balanceOf",
            "checkpoints",
            "decimals",
            "decreaseAllowance",
            "delegate",
            "delegateBySig",
            "delegates",
            "getCurrentVotes",
            "getPastTotalSupply",
            "getPastVotes",
            "getPriorVotes",
            "getVotes",
            "increaseAllowance",
            "name",
            "nonces",
            "numCheckpoints",
            "permit",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "f052c288": {
        "name": "ERC4626DecimalMock",
        "selector": "f052c288",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "mockBurn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "mockMint",
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "decreaseAllowance",
            "deposit",
            "increaseAllowance",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "mockBurn",
            "mockMint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "12ab25d7": {
        "name": "ERC721Votes",
        "selector": "12ab25d7",
        "abi": [
            {"inputs": [], "name": "CheckpointUnorderedInsertion", "type": "error"},
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                    {"internalType": "uint48", "name": "clock", "type": "uint48"},
                ],
                "name": "ERC5805FutureLookup",
                "type": "error",
            },
            {"inputs": [], "name": "ERC6372InconsistentClock", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint8", "name": "bits", "type": "uint8"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "SafeCastOverflowedUintDowncast",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"}
                ],
                "name": "VotesExpiredSignature",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "name": "delegator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromDelegate",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toDelegate",
                        "type": "address",
                    },
                ],
                "name": "DelegateChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "previousBalance",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "newBalance",
                        "type": "uint256",
                    },
                ],
                "name": "DelegateVotesChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "CLOCK_MODE",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "clock",
                "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"}
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "CLOCK_MODE",
            "approve",
            "balanceOf",
            "clock",
            "delegate",
            "delegateBySig",
            "delegates",
            "eip712Domain",
            "getApproved",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
            "isApprovedForAll",
            "name",
            "nonces",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "8e0a4fe1": {
        "name": "ERC721URIStorageMock",
        "selector": "8e0a4fe1",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_fromTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_toTokenId",
                        "type": "uint256",
                    },
                ],
                "name": "BatchMetadataUpdate",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_tokenId",
                        "type": "uint256",
                    }
                ],
                "name": "MetadataUpdate",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "newBaseTokenURI",
                        "type": "string",
                    }
                ],
                "name": "setBaseURI",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "setBaseURI",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "1626ba7e": {
        "name": "ERC1271MaliciousMock",
        "selector": "1626ba7e",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "", "type": "bytes32"},
                    {"internalType": "bytes", "name": "", "type": "bytes"},
                ],
                "name": "isValidSignature",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "pure",
                "type": "function",
            }
        ],
        "functions_names": ["isValidSignature"],
    },
    "fe733816": {
        "name": "ERC721EnumerableMock",
        "selector": "fe733816",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "baseURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "exists",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "bytes", "name": "_data", "type": "bytes"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "newBaseTokenURI",
                        "type": "string",
                    }
                ],
                "name": "setBaseURI",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [
                    {"internalType": "uint256", "name": "index", "type": "uint256"}
                ],
                "name": "tokenByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "baseURI",
            "burn",
            "exists",
            "getApproved",
            "isApprovedForAll",
            "mint",
            "name",
            "ownerOf",
            "safeMint",
            "safeMint",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "setBaseURI",
            "symbol",
            "tokenByIndex",
            "tokenOfOwnerByIndex",
            "tokenURI",
            "totalSupply",
            "transferFrom",
        ],
    },
    "65289bcd": {
        "name": "ERC20ReturnTrueMock",
        "selector": "65289bcd",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "allowance_", "type": "uint256"}
                ],
                "name": "setAllowance",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "setAllowance",
            "transfer",
            "transferFrom",
        ],
    },
    "690aaefd": {
        "name": "ERC20Wrapper",
        "selector": "690aaefd",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "ERC20InvalidUnderlying",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "SafeERC20FailedOperation",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "depositFor",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "underlying",
                "outputs": [
                    {"internalType": "contract IERC20", "name": "", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "withdrawTo",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "depositFor",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
            "underlying",
            "withdrawTo",
        ],
    },
    "01ffc9a7": {
        "name": "ERC165MissingData",
        "selector": "01ffc9a7",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["supportsInterface"],
    },
    "3273d15c": {
        "name": "ERC20PresetFixedSupply",
        "selector": "3273d15c",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burnFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "burnFrom",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "71aa57a7": {
        "name": "ERC1820ImplementerMock",
        "selector": "71aa57a7",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "bytes32",
                        "name": "interfaceHash",
                        "type": "bytes32",
                    },
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "canImplementInterfaceForAddress",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "bytes32",
                        "name": "interfaceHash",
                        "type": "bytes32",
                    },
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "registerInterfaceForAddress",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "canImplementInterfaceForAddress",
            "registerInterfaceForAddress",
        ],
    },
    "2f33d60e": {
        "name": "ERC20FlashMintMock",
        "selector": "2f33d60e",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "maxLoan", "type": "uint256"}
                ],
                "name": "ERC3156ExceededMaxLoan",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC3156InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "ERC3156UnsupportedToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "flashFee",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "contract IERC3156FlashBorrower",
                        "name": "receiver",
                        "type": "address",
                    },
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "flashLoan",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "maxFlashLoan",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "setFlashFee",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "setFlashFeeReceiver",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "flashFee",
            "flashLoan",
            "increaseAllowance",
            "maxFlashLoan",
            "name",
            "setFlashFee",
            "setFlashFeeReceiver",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "d73f4e3a": {
        "name": "ERC1155URIStorage",
        "selector": "d73f4e3a",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC1155InsufficientApprovalForAll",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC1155InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC1155InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "idsLength", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "valuesLength",
                        "type": "uint256",
                    },
                ],
                "name": "ERC1155InvalidArrayLength",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC1155InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC1155InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC1155InvalidSender",
                "type": "error",
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
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
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "isApprovedForAll",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "uri",
        ],
    },
    "d385a1c6": {
        "name": "ERC721Mock",
        "selector": "d385a1c6",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "baseURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "exists",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "bytes", "name": "_data", "type": "bytes"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "baseURI",
            "burn",
            "exists",
            "getApproved",
            "isApprovedForAll",
            "mint",
            "name",
            "ownerOf",
            "safeMint",
            "safeMint",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "d9b67a26": {
        "name": "IERC1155",
        "selector": "d9b67a26",
        "abi": [
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
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
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "isApprovedForAll",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
        ],
    },
    "23e30c8b": {
        "name": "ERC3156FlashBorrowerMock",
        "selector": "23e30c8b",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bool", "name": "enableReturn", "type": "bool"},
                    {"internalType": "bool", "name": "enableApprove", "type": "bool"},
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "token",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "BalanceOf",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "token",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "TotalSupply",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "uint256", "name": "fee", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onFlashLoan",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["onFlashLoan"],
    },
    "84b0196e": {
        "name": "IERC5267",
        "selector": "84b0196e",
        "abi": [
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": ["eip712Domain"],
    },
    "2a55205a": {
        "name": "ERC2981",
        "selector": "2a55205a",
        "abi": [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "numerator", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "denominator",
                        "type": "uint256",
                    },
                ],
                "name": "ERC2981InvalidDefaultRoyalty",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC2981InvalidDefaultRoyaltyReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint256", "name": "numerator", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "denominator",
                        "type": "uint256",
                    },
                ],
                "name": "ERC2981InvalidTokenRoyalty",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "ERC2981InvalidTokenRoyaltyReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint256", "name": "salePrice", "type": "uint256"},
                ],
                "name": "royaltyInfo",
                "outputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": ["royaltyInfo"],
    },
    "0929daa4": {
        "name": "ERC20ReturnFalseMock",
        "selector": "0929daa4",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "pure",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "pure",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "pure",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "9d8ff7da": {
        "name": "IERC2612",
        "selector": "9d8ff7da",
        "abi": [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["DOMAIN_SEPARATOR", "nonces", "permit"],
    },
    "8a3350b0": {
        "name": "ERC777",
        "selector": "8a3350b0",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "holder", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "authorizeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "tokenHolder",
                        "type": "address",
                    }
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "pure",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "defaultOperators",
                "outputs": [
                    {"internalType": "address[]", "name": "", "type": "address[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "granularity",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "tokenHolder",
                        "type": "address",
                    },
                ],
                "name": "isOperatorFor",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorBurn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorSend",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "revokeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "send",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "holder", "type": "address"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "authorizeOperator",
            "balanceOf",
            "burn",
            "decimals",
            "defaultOperators",
            "granularity",
            "isOperatorFor",
            "name",
            "operatorBurn",
            "operatorSend",
            "revokeOperator",
            "send",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "88cc3f92": {
        "name": "ERC721VotesMock",
        "selector": "88cc3f92",
        "abi": [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getChainId",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    }
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "approve",
            "balanceOf",
            "burn",
            "delegate",
            "delegateBySig",
            "delegates",
            "getApproved",
            "getChainId",
            "getPastTotalSupply",
            "getPastVotes",
            "getTotalSupply",
            "getVotes",
            "isApprovedForAll",
            "mint",
            "name",
            "nonces",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "3528c9cb": {
        "name": "ERC165InterfacesSupported",
        "selector": "3528c9cb",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "bytes4[]",
                        "name": "interfaceIds",
                        "type": "bytes4[]",
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {
                "inputs": [],
                "name": "INTERFACE_ID_ERC165",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": ["INTERFACE_ID_ERC165", "supportsInterface"],
    },
    "9964273a": {
        "name": "ERC721Burnable",
        "selector": "9964273a",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "burn",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "b7774ea0": {
        "name": "ERC2771ContextMock",
        "selector": "b7774ea0",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "trustedForwarder",
                        "type": "address",
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "integerValue",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "string",
                        "name": "stringValue",
                        "type": "string",
                    },
                ],
                "name": "Data",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    }
                ],
                "name": "Sender",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "forwarder", "type": "address"}
                ],
                "name": "isTrustedForwarder",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "integerValue",
                        "type": "uint256",
                    },
                    {"internalType": "string", "name": "stringValue", "type": "string"},
                ],
                "name": "msgData",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "msgSender",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["isTrustedForwarder", "msgData", "msgSender"],
    },
    "876511e9": {
        "name": "ERC721Pausable",
        "selector": "876511e9",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {"inputs": [], "name": "EnforcedPause", "type": "error"},
            {"inputs": [], "name": "ExpectedPause", "type": "error"},
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Paused",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Unpaused",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "paused",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "2a55205a": {
        "name": "IERC2981",
        "selector": "2a55205a",
        "abi": [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint256", "name": "salePrice", "type": "uint256"},
                ],
                "name": "royaltyInfo",
                "outputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "royaltyAmount",
                        "type": "uint256",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["royaltyInfo"],
    },
    "01ffc9a7": {
        "name": "ERC165ReturnBombMock",
        "selector": "01ffc9a7",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "pure",
                "type": "function",
            }
        ],
        "functions_names": ["supportsInterface"],
    },
    "5ead35bc": {
        "name": "ERC20VotesTimestampMock",
        "selector": "5ead35bc",
        "abi": [
            {"inputs": [], "name": "CheckpointUnorderedInsertion", "type": "error"},
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "increasedSupply",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "cap", "type": "uint256"},
                ],
                "name": "ERC20ExceededSafeSupply",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                    {"internalType": "uint48", "name": "clock", "type": "uint48"},
                ],
                "name": "ERC5805FutureLookup",
                "type": "error",
            },
            {"inputs": [], "name": "ERC6372InconsistentClock", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint8", "name": "bits", "type": "uint8"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "SafeCastOverflowedUintDowncast",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"}
                ],
                "name": "VotesExpiredSignature",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromDelegate",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toDelegate",
                        "type": "address",
                    },
                ],
                "name": "DelegateChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "previousBalance",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "newBalance",
                        "type": "uint256",
                    },
                ],
                "name": "DelegateVotesChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "CLOCK_MODE",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint32", "name": "pos", "type": "uint32"},
                ],
                "name": "checkpoints",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "_key",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint224",
                                "name": "_value",
                                "type": "uint224",
                            },
                        ],
                        "internalType": "struct Checkpoints.Checkpoint224",
                        "name": "",
                        "type": "tuple",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "clock",
                "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"}
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "numCheckpoints",
                "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "CLOCK_MODE",
            "allowance",
            "approve",
            "balanceOf",
            "checkpoints",
            "clock",
            "decimals",
            "decreaseAllowance",
            "delegate",
            "delegateBySig",
            "delegates",
            "eip712Domain",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
            "increaseAllowance",
            "name",
            "nonces",
            "numCheckpoints",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "53f5afb1": {
        "name": "ERC4626Mock",
        "selector": "53f5afb1",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "underlying", "type": "address"}
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxDeposit",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxRedeem",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxWithdraw",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {"inputs": [], "name": "MathOverflowedMulDiv", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "SafeERC20FailedOperation",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Deposit",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Withdraw",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "burn",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "decreaseAllowance",
            "deposit",
            "increaseAllowance",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "mint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "9d8ff7da": {
        "name": "IERC20Permit",
        "selector": "9d8ff7da",
        "abi": [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["DOMAIN_SEPARATOR", "nonces", "permit"],
    },
    "313ce567": {
        "name": "ERC20ExcessDecimalsMock",
        "selector": "313ce567",
        "abi": [
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "pure",
                "type": "function",
            }
        ],
        "functions_names": ["decimals"],
    },
    "249cb3fa": {
        "name": "IERC1820Implementer",
        "selector": "249cb3fa",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "bytes32",
                        "name": "interfaceHash",
                        "type": "bytes32",
                    },
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "canImplementInterfaceForAddress",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["canImplementInterfaceForAddress"],
    },
    "e58e113c": {
        "name": "IERC777",
        "selector": "e58e113c",
        "abi": [
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
                        "name": "tokenHolder",
                        "type": "address",
                    },
                ],
                "name": "AuthorizedOperator",
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
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes",
                    },
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "operatorData",
                        "type": "bytes",
                    },
                ],
                "name": "Burned",
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
                        "name": "to",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes",
                    },
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "operatorData",
                        "type": "bytes",
                    },
                ],
                "name": "Minted",
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
                        "name": "tokenHolder",
                        "type": "address",
                    },
                ],
                "name": "RevokedOperator",
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
                        "name": "amount",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes",
                    },
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "operatorData",
                        "type": "bytes",
                    },
                ],
                "name": "Sent",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "authorizeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "defaultOperators",
                "outputs": [
                    {"internalType": "address[]", "name": "", "type": "address[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "granularity",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "tokenHolder",
                        "type": "address",
                    },
                ],
                "name": "isOperatorFor",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorBurn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorSend",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "revokeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "send",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "authorizeOperator",
            "balanceOf",
            "burn",
            "defaultOperators",
            "granularity",
            "isOperatorFor",
            "name",
            "operatorBurn",
            "operatorSend",
            "revokeOperator",
            "send",
            "symbol",
            "totalSupply",
        ],
    },
    "ed3dea35": {
        "name": "ERC20FlashMint",
        "selector": "ed3dea35",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "maxLoan", "type": "uint256"}
                ],
                "name": "ERC3156ExceededMaxLoan",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC3156InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "ERC3156UnsupportedToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "flashFee",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "contract IERC3156FlashBorrower",
                        "name": "receiver",
                        "type": "address",
                    },
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "flashLoan",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "maxFlashLoan",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "flashFee",
            "flashLoan",
            "increaseAllowance",
            "maxFlashLoan",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "150b7a02": {
        "name": "ERC721Holder",
        "selector": "150b7a02",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                    {"internalType": "bytes", "name": "", "type": "bytes"},
                ],
                "name": "onERC721Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["onERC721Received"],
    },
    "80ac58cd": {
        "name": "IERC4906",
        "selector": "80ac58cd",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_fromTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_toTokenId",
                        "type": "uint256",
                    },
                ],
                "name": "BatchMetadataUpdate",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_tokenId",
                        "type": "uint256",
                    }
                ],
                "name": "MetadataUpdate",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [
                    {"internalType": "uint256", "name": "balance", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "transferFrom",
        ],
    },
    "0a7f6bd0": {
        "name": "ERC20VotesMock",
        "selector": "0a7f6bd0",
        "abi": [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint32", "name": "pos", "type": "uint32"},
                ],
                "name": "checkpoints",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "fromBlock",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint224",
                                "name": "votes",
                                "type": "uint224",
                            },
                        ],
                        "internalType": "struct ERC20Votes.Checkpoint",
                        "name": "",
                        "type": "tuple",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getChainId",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    }
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "numCheckpoints",
                "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "checkpoints",
            "decimals",
            "decreaseAllowance",
            "delegate",
            "delegateBySig",
            "delegates",
            "getChainId",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
            "increaseAllowance",
            "mint",
            "name",
            "nonces",
            "numCheckpoints",
            "permit",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "dbf24b52": {
        "name": "ERC721Consecutive",
        "selector": "dbf24b52",
        "abi": [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "batchSize", "type": "uint256"},
                    {"internalType": "uint256", "name": "maxBatch", "type": "uint256"},
                ],
                "name": "ERC721ExceededMaxBatchMint",
                "type": "error",
            },
            {"inputs": [], "name": "ERC721ForbiddenBatchBurn", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenBatchMint", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenMint", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "internalType": "uint256",
                        "name": "fromTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "toTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromAddress",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toAddress",
                        "type": "address",
                    },
                ],
                "name": "ConsecutiveTransfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "150b7a02": {
        "name": "IERC721Receiver",
        "selector": "150b7a02",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC721Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["onERC721Received"],
    },
    "3c7bae4e": {
        "name": "ERC20Capped",
        "selector": "3c7bae4e",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "increasedSupply",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "cap", "type": "uint256"},
                ],
                "name": "ERC20ExceededCap",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "cap", "type": "uint256"}
                ],
                "name": "ERC20InvalidCap",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "cap",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "cap",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "86bfc821": {
        "name": "ERC20PermitNoRevertMock",
        "selector": "86bfc821",
        "abi": [
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"}
                ],
                "name": "ERC2612ExpiredSignature",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "signer", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC2612InvalidSigner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permitThatMayRevert",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "eip712Domain",
            "increaseAllowance",
            "name",
            "nonces",
            "permit",
            "permitThatMayRevert",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "dbf24b52": {
        "name": "ERC721ConsecutiveNoConstructorMintMock",
        "selector": "dbf24b52",
        "abi": [
            {
                "inputs": [
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "symbol", "type": "string"},
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "batchSize", "type": "uint256"},
                    {"internalType": "uint256", "name": "maxBatch", "type": "uint256"},
                ],
                "name": "ERC721ExceededMaxBatchMint",
                "type": "error",
            },
            {"inputs": [], "name": "ERC721ForbiddenBatchBurn", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenBatchMint", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenMint", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "internalType": "uint256",
                        "name": "fromTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "toTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromAddress",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toAddress",
                        "type": "address",
                    },
                ],
                "name": "ConsecutiveTransfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "a3fcd631": {
        "name": "ERC721ConsecutiveEnumerableMock",
        "selector": "a3fcd631",
        "abi": [
            {
                "inputs": [
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "symbol", "type": "string"},
                    {
                        "internalType": "address[]",
                        "name": "receivers",
                        "type": "address[]",
                    },
                    {"internalType": "uint96[]", "name": "amounts", "type": "uint96[]"},
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {"inputs": [], "name": "CheckpointUnorderedInsertion", "type": "error"},
            {
                "inputs": [],
                "name": "ERC721EnumerableForbiddenBatchMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "batchSize", "type": "uint256"},
                    {"internalType": "uint256", "name": "maxBatch", "type": "uint256"},
                ],
                "name": "ERC721ExceededMaxBatchMint",
                "type": "error",
            },
            {"inputs": [], "name": "ERC721ForbiddenBatchBurn", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenBatchMint", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenMint", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "ERC721OutOfBoundsIndex",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "internalType": "uint256",
                        "name": "fromTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "toTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromAddress",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toAddress",
                        "type": "address",
                    },
                ],
                "name": "ConsecutiveTransfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "index", "type": "uint256"}
                ],
                "name": "tokenByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenByIndex",
            "tokenOfOwnerByIndex",
            "tokenURI",
            "totalSupply",
            "transferFrom",
        ],
    },
    "942e8b22": {
        "name": "IERC20Metadata",
        "selector": "942e8b22",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "0929daa4": {
        "name": "ERC20DecimalsMock",
        "selector": "0929daa4",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "27a6bfb2": {
        "name": "ERC1155Mock",
        "selector": "27a6bfb2",
        "abi": [
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                ],
                "name": "burnBatch",
                "outputs": [],
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
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mintBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [
                    {"internalType": "string", "name": "newuri", "type": "string"}
                ],
                "name": "setURI",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "burn",
            "burnBatch",
            "isApprovedForAll",
            "mint",
            "mintBatch",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "setURI",
            "uri",
        ],
    },
    "4e2312e0": {
        "name": "IERC1155Receiver",
        "selector": "4e2312e0",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC1155BatchReceived",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC1155Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["onERC1155BatchReceived", "onERC1155Received"],
    },
    "214cdb80": {
        "name": "ERC165StorageMock",
        "selector": "214cdb80",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "registerInterface",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["registerInterface"],
    },
    "d1a4bb67": {
        "name": "ERC777SenderRecipientMock",
        "selector": "d1a4bb67",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "contract IERC777",
                        "name": "token",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "bytes32",
                        "name": "interfaceHash",
                        "type": "bytes32",
                    },
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "canImplementInterfaceForAddress",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "recipientFor",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"}
                ],
                "name": "registerRecipient",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "registerSender",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "contract IERC777",
                        "name": "token",
                        "type": "address",
                    },
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "send",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "senderFor",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bool", "name": "shouldRevert", "type": "bool"}
                ],
                "name": "setShouldRevertReceive",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bool", "name": "shouldRevert", "type": "bool"}
                ],
                "name": "setShouldRevertSend",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "tokensReceived",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "tokensToSend",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "burn",
            "canImplementInterfaceForAddress",
            "recipientFor",
            "registerRecipient",
            "registerSender",
            "send",
            "senderFor",
            "setShouldRevertReceive",
            "setShouldRevertSend",
            "tokensReceived",
            "tokensToSend",
        ],
    },
    "55be801f": {
        "name": "ERC20Pausable",
        "selector": "55be801f",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {"inputs": [], "name": "EnforcedPause", "type": "error"},
            {"inputs": [], "name": "ExpectedPause", "type": "error"},
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Paused",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Unpaused",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "paused",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "paused",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "c6e7ee66": {
        "name": "ERC20VotesCompMock",
        "selector": "c6e7ee66",
        "abi": [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint32", "name": "pos", "type": "uint32"},
                ],
                "name": "checkpoints",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "fromBlock",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint224",
                                "name": "votes",
                                "type": "uint224",
                            },
                        ],
                        "internalType": "struct ERC20Votes.Checkpoint",
                        "name": "",
                        "type": "tuple",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getChainId",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getCurrentVotes",
                "outputs": [{"internalType": "uint96", "name": "", "type": "uint96"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    }
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "name": "getPriorVotes",
                "outputs": [{"internalType": "uint96", "name": "", "type": "uint96"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "numCheckpoints",
                "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "checkpoints",
            "decimals",
            "decreaseAllowance",
            "delegate",
            "delegateBySig",
            "delegates",
            "getChainId",
            "getCurrentVotes",
            "getPastTotalSupply",
            "getPastVotes",
            "getPriorVotes",
            "getVotes",
            "increaseAllowance",
            "mint",
            "name",
            "nonces",
            "numCheckpoints",
            "permit",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "0929daa4": {
        "name": "ERC20ForceApproveMock",
        "selector": "0929daa4",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "d73f4e3a": {
        "name": "ERC1155",
        "selector": "d73f4e3a",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC1155InsufficientApprovalForAll",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC1155InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC1155InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "idsLength", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "valuesLength",
                        "type": "uint256",
                    },
                ],
                "name": "ERC1155InvalidArrayLength",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC1155InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC1155InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC1155InvalidSender",
                "type": "error",
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
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
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "isApprovedForAll",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "uri",
        ],
    },
    "e4143091": {
        "name": "IERC3156FlashLender",
        "selector": "e4143091",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "flashFee",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "contract IERC3156FlashBorrower",
                        "name": "receiver",
                        "type": "address",
                    },
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "flashLoan",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "maxFlashLoan",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": ["flashFee", "flashLoan", "maxFlashLoan"],
    },
    "65d2cb11": {
        "name": "ERC20WrapperMock",
        "selector": "65d2cb11",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "depositFor",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "recover",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "underlying",
                "outputs": [
                    {"internalType": "contract IERC20", "name": "", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "withdrawTo",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "depositFor",
            "increaseAllowance",
            "name",
            "recover",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
            "underlying",
            "withdrawTo",
        ],
    },
    "4e2312e0": {
        "name": "ERC1155ReceiverMock",
        "selector": "4e2312e0",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "recRetval", "type": "bytes4"},
                    {"internalType": "bytes4", "name": "batRetval", "type": "bytes4"},
                    {
                        "internalType": "enum ERC1155ReceiverMock.RevertType",
                        "name": "error",
                        "type": "uint8",
                    },
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {
                "inputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "name": "CustomError",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "operator",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "from",
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
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "gas",
                        "type": "uint256",
                    },
                ],
                "name": "BatchReceived",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "operator",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "from",
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
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "gas",
                        "type": "uint256",
                    },
                ],
                "name": "Received",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC1155BatchReceived",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC1155Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["onERC1155BatchReceived", "onERC1155Received"],
    },
    "04cc9298": {
        "name": "ERC721RoyaltyMock",
        "selector": "04cc9298",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "deleteDefaultRoyalty",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "_tokenId", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "_salePrice",
                        "type": "uint256",
                    },
                ],
                "name": "royaltyInfo",
                "outputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint96", "name": "fraction", "type": "uint96"},
                ],
                "name": "setDefaultRoyalty",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint96", "name": "fraction", "type": "uint96"},
                ],
                "name": "setTokenRoyalty",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "burn",
            "deleteDefaultRoyalty",
            "getApproved",
            "isApprovedForAll",
            "mint",
            "name",
            "ownerOf",
            "royaltyInfo",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "setDefaultRoyalty",
            "setTokenRoyalty",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "c02c866a": {
        "name": "ERC1155PausableMock",
        "selector": "c02c866a",
        "abi": [
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                ],
                "name": "burnBatch",
                "outputs": [],
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
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mintBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [
                    {"internalType": "string", "name": "newuri", "type": "string"}
                ],
                "name": "setURI",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "unpause",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "burn",
            "burnBatch",
            "isApprovedForAll",
            "mint",
            "mintBatch",
            "pause",
            "paused",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "setURI",
            "unpause",
            "uri",
        ],
    },
    "33a073c9": {
        "name": "ERC20PausableMock",
        "selector": "33a073c9",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "unpause",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "mint",
            "name",
            "pause",
            "paused",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
            "unpause",
        ],
    },
    "dbf24b52": {
        "name": "ERC721URIStorage",
        "selector": "dbf24b52",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_fromTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_toTokenId",
                        "type": "uint256",
                    },
                ],
                "name": "BatchMetadataUpdate",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_tokenId",
                        "type": "uint256",
                    }
                ],
                "name": "MetadataUpdate",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "4e2312e0": {
        "name": "ERC1155Receiver",
        "selector": "4e2312e0",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC1155BatchReceived",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC1155Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["onERC1155BatchReceived", "onERC1155Received"],
    },
    "da287a1d": {
        "name": "IERC6372",
        "selector": "da287a1d",
        "abi": [
            {
                "inputs": [],
                "name": "CLOCK_MODE",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "clock",
                "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": ["CLOCK_MODE", "clock"],
    },
    "182e8a08": {
        "name": "ERC1271WalletMock",
        "selector": "182e8a08",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "originalOwner",
                        "type": "address",
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "OwnableInvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "OwnableUnauthorizedAccount",
                "type": "error",
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
                "inputs": [
                    {"internalType": "bytes32", "name": "hash", "type": "bytes32"},
                    {"internalType": "bytes", "name": "signature", "type": "bytes"},
                ],
                "name": "isValidSignature",
                "outputs": [
                    {"internalType": "bytes4", "name": "magicValue", "type": "bytes4"}
                ],
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
                "name": "renounceOwnership",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "newOwner", "type": "address"}
                ],
                "name": "transferOwnership",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "isValidSignature",
            "owner",
            "renounceOwnership",
            "transferOwnership",
        ],
    },
    "12ab25d7": {
        "name": "ERC721VotesTimestampMock",
        "selector": "12ab25d7",
        "abi": [
            {"inputs": [], "name": "CheckpointUnorderedInsertion", "type": "error"},
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                    {"internalType": "uint48", "name": "clock", "type": "uint48"},
                ],
                "name": "ERC5805FutureLookup",
                "type": "error",
            },
            {"inputs": [], "name": "ERC6372InconsistentClock", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint8", "name": "bits", "type": "uint8"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "SafeCastOverflowedUintDowncast",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"}
                ],
                "name": "VotesExpiredSignature",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "name": "delegator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromDelegate",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toDelegate",
                        "type": "address",
                    },
                ],
                "name": "DelegateChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "previousBalance",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "newBalance",
                        "type": "uint256",
                    },
                ],
                "name": "DelegateVotesChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "CLOCK_MODE",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "clock",
                "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"}
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "CLOCK_MODE",
            "approve",
            "balanceOf",
            "clock",
            "delegate",
            "delegateBySig",
            "delegates",
            "eip712Domain",
            "getApproved",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
            "isApprovedForAll",
            "name",
            "nonces",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "8a3350b0": {
        "name": "ERC777PresetFixedSupply",
        "selector": "8a3350b0",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "holder", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "authorizeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "tokenHolder",
                        "type": "address",
                    }
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "pure",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "defaultOperators",
                "outputs": [
                    {"internalType": "address[]", "name": "", "type": "address[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "granularity",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "tokenHolder",
                        "type": "address",
                    },
                ],
                "name": "isOperatorFor",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorBurn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "operatorSend",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "revokeOperator",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "send",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "holder", "type": "address"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "authorizeOperator",
            "balanceOf",
            "burn",
            "decimals",
            "defaultOperators",
            "granularity",
            "isOperatorFor",
            "name",
            "operatorBurn",
            "operatorSend",
            "revokeOperator",
            "send",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "150b7a02": {
        "name": "ERC721ReceiverMock",
        "selector": "150b7a02",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "retval", "type": "bytes4"},
                    {
                        "internalType": "enum ERC721ReceiverMock.RevertType",
                        "name": "error",
                        "type": "uint8",
                    },
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {
                "inputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "name": "CustomError",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "operator",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "from",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "bytes",
                        "name": "data",
                        "type": "bytes",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "gas",
                        "type": "uint256",
                    },
                ],
                "name": "Received",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onERC721Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["onERC721Received"],
    },
    "493600a4": {
        "name": "ERC1155Burnable",
        "selector": "493600a4",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC1155InsufficientApprovalForAll",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC1155InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC1155InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "idsLength", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "valuesLength",
                        "type": "uint256",
                    },
                ],
                "name": "ERC1155InvalidArrayLength",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC1155InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC1155InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC1155InvalidSender",
                "type": "error",
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                ],
                "name": "burnBatch",
                "outputs": [],
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
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "burn",
            "burnBatch",
            "isApprovedForAll",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "uri",
        ],
    },
    "01ffc9a7": {
        "name": "ERC165",
        "selector": "01ffc9a7",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["supportsInterface"],
    },
    "70a649ce": {
        "name": "ERC1155PresetMinterPauser",
        "selector": "70a649ce",
        "abi": [
            {
                "inputs": [],
                "name": "DEFAULT_ADMIN_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "MINTER_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "PAUSER_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                ],
                "name": "burnBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"}
                ],
                "name": "getRoleAdmin",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "getRoleMember",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"}
                ],
                "name": "getRoleMemberCount",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "grantRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "hasRole",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mintBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "renounceRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "revokeRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [],
                "name": "unpause",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "DEFAULT_ADMIN_ROLE",
            "MINTER_ROLE",
            "PAUSER_ROLE",
            "balanceOf",
            "balanceOfBatch",
            "burn",
            "burnBatch",
            "getRoleAdmin",
            "getRoleMember",
            "getRoleMemberCount",
            "grantRole",
            "hasRole",
            "isApprovedForAll",
            "mint",
            "mintBatch",
            "pause",
            "paused",
            "renounceRole",
            "revokeRole",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "unpause",
            "uri",
        ],
    },
    "171c304d": {
        "name": "ERC721Wrapper",
        "selector": "171c304d",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "ERC721UnsupportedToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256[]",
                        "name": "tokenIds",
                        "type": "uint256[]",
                    },
                ],
                "name": "depositFor",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "bytes", "name": "", "type": "bytes"},
                ],
                "name": "onERC721Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "underlying",
                "outputs": [
                    {"internalType": "contract IERC721", "name": "", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256[]",
                        "name": "tokenIds",
                        "type": "uint256[]",
                    },
                ],
                "name": "withdrawTo",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "depositFor",
            "getApproved",
            "isApprovedForAll",
            "name",
            "onERC721Received",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
            "underlying",
            "withdrawTo",
        ],
    },
    "8ef63f04": {
        "name": "ERC4626FeesMock",
        "selector": "8ef63f04",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxDeposit",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxRedeem",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxWithdraw",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {"inputs": [], "name": "MathOverflowedMulDiv", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "SafeERC20FailedOperation",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Deposit",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Withdraw",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "decreaseAllowance",
            "deposit",
            "increaseAllowance",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "7b04a2d0": {
        "name": "IERC1363Spender",
        "selector": "7b04a2d0",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onApprovalReceived",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["onApprovalReceived"],
    },
    "0929daa4": {
        "name": "ERC20",
        "selector": "0929daa4",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "8ef63f04": {
        "name": "ERC4626",
        "selector": "8ef63f04",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxDeposit",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxRedeem",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxWithdraw",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {"inputs": [], "name": "MathOverflowedMulDiv", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "SafeERC20FailedOperation",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Deposit",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Withdraw",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "decreaseAllowance",
            "deposit",
            "increaseAllowance",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "0929daa4": {
        "name": "ERC20NoReturnMock",
        "selector": "0929daa4",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "52d1902d": {
        "name": "IERC1822Proxiable",
        "selector": "52d1902d",
        "abi": [
            {
                "inputs": [],
                "name": "proxiableUUID",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["proxiableUUID"],
    },
    "75ab9782": {
        "name": "IERC777Sender",
        "selector": "75ab9782",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "tokensToSend",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["tokensToSend"],
    },
    "a0aec90e": {
        "name": "ERC20PermitMock",
        "selector": "a0aec90e",
        "abi": [
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "getChainId",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "getChainId",
            "increaseAllowance",
            "name",
            "nonces",
            "permit",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "67c4067b": {
        "name": "ERC20VotesLegacyMock",
        "selector": "67c4067b",
        "abi": [
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"}
                ],
                "name": "ERC2612ExpiredSignature",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "signer", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC2612InvalidSigner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint8", "name": "bits", "type": "uint8"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "SafeCastOverflowedUintDowncast",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"}
                ],
                "name": "VotesExpiredSignature",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromDelegate",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toDelegate",
                        "type": "address",
                    },
                ],
                "name": "DelegateChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "previousBalance",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "newBalance",
                        "type": "uint256",
                    },
                ],
                "name": "DelegateVotesChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint32", "name": "pos", "type": "uint32"},
                ],
                "name": "checkpoints",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "fromBlock",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint224",
                                "name": "votes",
                                "type": "uint224",
                            },
                        ],
                        "internalType": "struct ERC20VotesLegacyMock.Checkpoint",
                        "name": "",
                        "type": "tuple",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    }
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "numCheckpoints",
                "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "allowance",
            "approve",
            "balanceOf",
            "checkpoints",
            "decimals",
            "decreaseAllowance",
            "delegate",
            "delegateBySig",
            "delegates",
            "eip712Domain",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
            "increaseAllowance",
            "name",
            "nonces",
            "numCheckpoints",
            "permit",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "3273d15c": {
        "name": "ERC20BurnableMock",
        "selector": "3273d15c",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burnFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "burnFrom",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "1626ba7e": {
        "name": "IERC1271",
        "selector": "1626ba7e",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "hash", "type": "bytes32"},
                    {"internalType": "bytes", "name": "signature", "type": "bytes"},
                ],
                "name": "isValidSignature",
                "outputs": [
                    {"internalType": "bytes4", "name": "magicValue", "type": "bytes4"}
                ],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["isValidSignature"],
    },
    "4e2312e0": {
        "name": "ERC1155Holder",
        "selector": "4e2312e0",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"},
                    {"internalType": "bytes", "name": "", "type": "bytes"},
                ],
                "name": "onERC1155BatchReceived",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                    {"internalType": "bytes", "name": "", "type": "bytes"},
                ],
                "name": "onERC1155Received",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": ["onERC1155BatchReceived", "onERC1155Received"],
    },
    "80ac58cd": {
        "name": "IERC721",
        "selector": "80ac58cd",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [
                    {"internalType": "uint256", "name": "balance", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "transferFrom",
        ],
    },
    "4e3c7f6c": {
        "name": "ERC721ConsecutiveMock",
        "selector": "4e3c7f6c",
        "abi": [
            {
                "inputs": [
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "symbol", "type": "string"},
                    {"internalType": "uint96", "name": "offset", "type": "uint96"},
                    {
                        "internalType": "address[]",
                        "name": "delegates",
                        "type": "address[]",
                    },
                    {
                        "internalType": "address[]",
                        "name": "receivers",
                        "type": "address[]",
                    },
                    {"internalType": "uint96[]", "name": "amounts", "type": "uint96[]"},
                ],
                "stateMutability": "nonpayable",
                "type": "constructor",
            },
            {"inputs": [], "name": "CheckpointUnorderedInsertion", "type": "error"},
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                    {"internalType": "uint48", "name": "clock", "type": "uint48"},
                ],
                "name": "ERC5805FutureLookup",
                "type": "error",
            },
            {"inputs": [], "name": "ERC6372InconsistentClock", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "batchSize", "type": "uint256"},
                    {"internalType": "uint256", "name": "maxBatch", "type": "uint256"},
                ],
                "name": "ERC721ExceededMaxBatchMint",
                "type": "error",
            },
            {"inputs": [], "name": "ERC721ForbiddenBatchBurn", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenBatchMint", "type": "error"},
            {"inputs": [], "name": "ERC721ForbiddenMint", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {"inputs": [], "name": "EnforcedPause", "type": "error"},
            {"inputs": [], "name": "ExpectedPause", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint8", "name": "bits", "type": "uint8"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "SafeCastOverflowedUintDowncast",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"}
                ],
                "name": "VotesExpiredSignature",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "internalType": "uint256",
                        "name": "fromTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "toTokenId",
                        "type": "uint256",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromAddress",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toAddress",
                        "type": "address",
                    },
                ],
                "name": "ConsecutiveTransfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromDelegate",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toDelegate",
                        "type": "address",
                    },
                ],
                "name": "DelegateChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "previousBalance",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "newBalance",
                        "type": "uint256",
                    },
                ],
                "name": "DelegateVotesChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Paused",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "address",
                        "name": "account",
                        "type": "address",
                    }
                ],
                "name": "Unpaused",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "CLOCK_MODE",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "clock",
                "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"}
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "CLOCK_MODE",
            "approve",
            "balanceOf",
            "clock",
            "delegate",
            "delegateBySig",
            "delegates",
            "eip712Domain",
            "getApproved",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
            "isApprovedForAll",
            "name",
            "nonces",
            "ownerOf",
            "paused",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "a3fcd631": {
        "name": "ERC721Enumerable",
        "selector": "a3fcd631",
        "abi": [
            {
                "inputs": [],
                "name": "ERC721EnumerableForbiddenBatchMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "ERC721OutOfBoundsIndex",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "index", "type": "uint256"}
                ],
                "name": "tokenByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenByIndex",
            "tokenOfOwnerByIndex",
            "tokenURI",
            "totalSupply",
            "transferFrom",
        ],
    },
    "3df97da7": {
        "name": "ERC1155Supply",
        "selector": "3df97da7",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC1155InsufficientApprovalForAll",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC1155InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC1155InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "idsLength", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "valuesLength",
                        "type": "uint256",
                    },
                ],
                "name": "ERC1155InvalidArrayLength",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC1155InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC1155InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC1155InvalidSender",
                "type": "error",
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"}
                ],
                "name": "exists",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"}
                ],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "exists",
            "isApprovedForAll",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "totalSupply",
            "totalSupply",
            "uri",
        ],
    },
    "23e30c8b": {
        "name": "IERC3156FlashBorrower",
        "selector": "23e30c8b",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "initiator", "type": "address"},
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "uint256", "name": "fee", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onFlashLoan",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["onFlashLoan"],
    },
    "8ef63f04": {
        "name": "ERC4626Fees",
        "selector": "8ef63f04",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxDeposit",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxRedeem",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxWithdraw",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {"inputs": [], "name": "MathOverflowedMulDiv", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "SafeERC20FailedOperation",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Deposit",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Withdraw",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "decreaseAllowance",
            "deposit",
            "increaseAllowance",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "a5bf8a7c": {
        "name": "ERC20MulticallMock",
        "selector": "a5bf8a7c",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes[]", "name": "data", "type": "bytes[]"}
                ],
                "name": "multicall",
                "outputs": [
                    {"internalType": "bytes[]", "name": "results", "type": "bytes[]"}
                ],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "multicall",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "88a7ca5c": {
        "name": "IERC1363Receiver",
        "selector": "88a7ca5c",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "onTransferReceived",
                "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["onTransferReceived"],
    },
    "623e6f86": {
        "name": "IERC1820Registry",
        "selector": "623e6f86",
        "abi": [
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
                        "internalType": "bytes32",
                        "name": "interfaceHash",
                        "type": "bytes32",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "implementer",
                        "type": "address",
                    },
                ],
                "name": "InterfaceImplementerSet",
                "type": "event",
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
                        "name": "newManager",
                        "type": "address",
                    },
                ],
                "name": "ManagerChanged",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "bytes32",
                        "name": "_interfaceHash",
                        "type": "bytes32",
                    },
                ],
                "name": "getInterfaceImplementer",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getManager",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"},
                ],
                "name": "implementsERC165Interface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"},
                ],
                "name": "implementsERC165InterfaceNoCache",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "interfaceName",
                        "type": "string",
                    }
                ],
                "name": "interfaceHash",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "pure",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "bytes32",
                        "name": "_interfaceHash",
                        "type": "bytes32",
                    },
                    {
                        "internalType": "address",
                        "name": "implementer",
                        "type": "address",
                    },
                ],
                "name": "setInterfaceImplementer",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "newManager",
                        "type": "address",
                    },
                ],
                "name": "setManager",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"},
                ],
                "name": "updateERC165Cache",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "getInterfaceImplementer",
            "getManager",
            "implementsERC165Interface",
            "implementsERC165InterfaceNoCache",
            "interfaceHash",
            "setInterfaceImplementer",
            "setManager",
            "updateERC165Cache",
        ],
    },
    "13f16e82": {
        "name": "IERC4626",
        "selector": "13f16e82",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Deposit",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Withdraw",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "assetTokenAddress",
                        "type": "address",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "maxDeposit",
                "outputs": [
                    {"internalType": "uint256", "name": "maxAssets", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "maxMint",
                "outputs": [
                    {"internalType": "uint256", "name": "maxShares", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [
                    {"internalType": "uint256", "name": "maxShares", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [
                    {"internalType": "uint256", "name": "maxAssets", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "totalManagedAssets",
                        "type": "uint256",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "deposit",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "8da5cb5b": {
        "name": "IERC5313",
        "selector": "8da5cb5b",
        "abi": [
            {
                "inputs": [],
                "name": "owner",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["owner"],
    },
    "5ead35bc": {
        "name": "ERC20Votes",
        "selector": "5ead35bc",
        "abi": [
            {"inputs": [], "name": "CheckpointUnorderedInsertion", "type": "error"},
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "increasedSupply",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "cap", "type": "uint256"},
                ],
                "name": "ERC20ExceededSafeSupply",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                    {"internalType": "uint48", "name": "clock", "type": "uint48"},
                ],
                "name": "ERC5805FutureLookup",
                "type": "error",
            },
            {"inputs": [], "name": "ERC6372InconsistentClock", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint8", "name": "bits", "type": "uint8"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "SafeCastOverflowedUintDowncast",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"}
                ],
                "name": "VotesExpiredSignature",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromDelegate",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toDelegate",
                        "type": "address",
                    },
                ],
                "name": "DelegateChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "previousBalance",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "newBalance",
                        "type": "uint256",
                    },
                ],
                "name": "DelegateVotesChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "CLOCK_MODE",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint32", "name": "pos", "type": "uint32"},
                ],
                "name": "checkpoints",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "_key",
                                "type": "uint32",
                            },
                            {
                                "internalType": "uint224",
                                "name": "_value",
                                "type": "uint224",
                            },
                        ],
                        "internalType": "struct Checkpoints.Checkpoint224",
                        "name": "",
                        "type": "tuple",
                    }
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "clock",
                "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"}
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "numCheckpoints",
                "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "CLOCK_MODE",
            "allowance",
            "approve",
            "balanceOf",
            "checkpoints",
            "clock",
            "decimals",
            "decreaseAllowance",
            "delegate",
            "delegateBySig",
            "delegates",
            "eip712Domain",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
            "increaseAllowance",
            "name",
            "nonces",
            "numCheckpoints",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "3327c9eb": {
        "name": "IERC5805",
        "selector": "3327c9eb",
        "abi": [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"}
                ],
                "name": "VotesExpiredSignature",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "fromDelegate",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "toDelegate",
                        "type": "address",
                    },
                ],
                "name": "DelegateChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "previousBalance",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "newBalance",
                        "type": "uint256",
                    },
                ],
                "name": "DelegateVotesChanged",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "CLOCK_MODE",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "clock",
                "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"}
                ],
                "name": "delegate",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "delegatee", "type": "address"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "delegateBySig",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "delegates",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"}
                ],
                "name": "getPastTotalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
                ],
                "name": "getPastVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "getVotes",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "CLOCK_MODE",
            "clock",
            "delegate",
            "delegateBySig",
            "delegates",
            "getPastTotalSupply",
            "getPastVotes",
            "getVotes",
        ],
    },
    "def66762": {
        "name": "ERC721PresetMinterPauserAutoId",
        "selector": "def66762",
        "abi": [
            {
                "inputs": [],
                "name": "DEFAULT_ADMIN_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "MINTER_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "PAUSER_ROLE",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"}
                ],
                "name": "getRoleAdmin",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "getRoleMember",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"}
                ],
                "name": "getRoleMemberCount",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "grantRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "hasRole",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"}
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
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
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "renounceRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "revokeRole",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "index", "type": "uint256"}
                ],
                "name": "tokenByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "unpause",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DEFAULT_ADMIN_ROLE",
            "MINTER_ROLE",
            "PAUSER_ROLE",
            "approve",
            "balanceOf",
            "burn",
            "getApproved",
            "getRoleAdmin",
            "getRoleMember",
            "getRoleMemberCount",
            "grantRole",
            "hasRole",
            "isApprovedForAll",
            "mint",
            "name",
            "ownerOf",
            "pause",
            "paused",
            "renounceRole",
            "revokeRole",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenByIndex",
            "tokenOfOwnerByIndex",
            "tokenURI",
            "totalSupply",
            "transferFrom",
            "unpause",
        ],
    },
    "3a27334d": {
        "name": "ERC1155BurnableMock",
        "selector": "3a27334d",
        "abi": [
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                ],
                "name": "burnBatch",
                "outputs": [],
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
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "burn",
            "burnBatch",
            "isApprovedForAll",
            "mint",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "uri",
        ],
    },
    "86170116": {
        "name": "IERC1363",
        "selector": "86170116",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approveAndCall",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "approveAndCall",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferAndCall",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "transferAndCall",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "transferFromAndCall",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFromAndCall",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "approveAndCall",
            "approveAndCall",
            "balanceOf",
            "totalSupply",
            "transfer",
            "transferAndCall",
            "transferAndCall",
            "transferFrom",
            "transferFromAndCall",
            "transferFromAndCall",
        ],
    },
    "7cbaa157": {
        "name": "ERC20CappedMock",
        "selector": "7cbaa157",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "cap",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "cap",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "mint",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "dbf24b52": {
        "name": "IERC721Metadata",
        "selector": "dbf24b52",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [
                    {"internalType": "uint256", "name": "balance", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "d42a4a11": {
        "name": "ERC20Mock",
        "selector": "d42a4a11",
        "abi": [
            {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "mint",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "249cb3fa": {
        "name": "ERC1820Implementer",
        "selector": "249cb3fa",
        "abi": [
            {
                "inputs": [
                    {
                        "internalType": "bytes32",
                        "name": "interfaceHash",
                        "type": "bytes32",
                    },
                    {"internalType": "address", "name": "account", "type": "address"},
                ],
                "name": "canImplementInterfaceForAddress",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["canImplementInterfaceForAddress"],
    },
    "f8a2c5ae": {
        "name": "IERC721Enumerable",
        "selector": "f8a2c5ae",
        "abi": [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [
                    {"internalType": "uint256", "name": "balance", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "uint256", "name": "index", "type": "uint256"}
                ],
                "name": "tokenByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "index", "type": "uint256"},
                ],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "tokenByIndex",
            "tokenOfOwnerByIndex",
            "totalSupply",
            "transferFrom",
        ],
    },
    "95c2d2e5": {
        "name": "ERC20SnapshotMock",
        "selector": "95c2d2e5",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "snapshotId",
                        "type": "uint256",
                    },
                ],
                "name": "balanceOfAt",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
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
                "name": "snapshot",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "snapshotId", "type": "uint256"}
                ],
                "name": "totalSupplyAt",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "balanceOfAt",
            "burn",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "mint",
            "name",
            "snapshot",
            "symbol",
            "totalSupply",
            "totalSupplyAt",
            "transfer",
            "transferFrom",
        ],
    },
    "0023de29": {
        "name": "IERC777Recipient",
        "selector": "0023de29",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {"internalType": "bytes", "name": "operatorData", "type": "bytes"},
                ],
                "name": "tokensReceived",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ],
        "functions_names": ["tokensReceived"],
    },
    "f1a76b08": {
        "name": "ERC721Royalty",
        "selector": "f1a76b08",
        "abi": [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "numerator", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "denominator",
                        "type": "uint256",
                    },
                ],
                "name": "ERC2981InvalidDefaultRoyalty",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC2981InvalidDefaultRoyaltyReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint256", "name": "numerator", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "denominator",
                        "type": "uint256",
                    },
                ],
                "name": "ERC2981InvalidTokenRoyalty",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "ERC2981InvalidTokenRoyaltyReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint256", "name": "salePrice", "type": "uint256"},
                ],
                "name": "royaltyInfo",
                "outputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "royaltyInfo",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "8ef63f04": {
        "name": "ERC4626OffsetMock",
        "selector": "8ef63f04",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxDeposit",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxMint",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxRedeem",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "uint256", "name": "max", "type": "uint256"},
                ],
                "name": "ERC4626ExceededMaxWithdraw",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {"inputs": [], "name": "MathOverflowedMulDiv", "type": "error"},
            {
                "inputs": [
                    {"internalType": "address", "name": "token", "type": "address"}
                ],
                "name": "SafeERC20FailedOperation",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Deposit",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "sender",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "receiver",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "assets",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "shares",
                        "type": "uint256",
                    },
                ],
                "name": "Withdraw",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "asset",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "convertToAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "convertToShares",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "deposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "", "type": "address"}],
                "name": "maxMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "maxWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewDeposit",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewMint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"}
                ],
                "name": "previewRedeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"}
                ],
                "name": "previewWithdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "shares", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "redeem",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalAssets",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "assets", "type": "uint256"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "withdraw",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "asset",
            "balanceOf",
            "convertToAssets",
            "convertToShares",
            "decimals",
            "decreaseAllowance",
            "deposit",
            "increaseAllowance",
            "maxDeposit",
            "maxMint",
            "maxRedeem",
            "maxWithdraw",
            "mint",
            "name",
            "previewDeposit",
            "previewMint",
            "previewRedeem",
            "previewWithdraw",
            "redeem",
            "symbol",
            "totalAssets",
            "totalSupply",
            "transfer",
            "transferFrom",
            "withdraw",
        ],
    },
    "dfd0330a": {
        "name": "ERC20Snapshot",
        "selector": "dfd0330a",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "snapshotId",
                        "type": "uint256",
                    },
                ],
                "name": "balanceOfAt",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "snapshotId", "type": "uint256"}
                ],
                "name": "totalSupplyAt",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "balanceOfAt",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "totalSupplyAt",
            "transfer",
            "transferFrom",
        ],
    },
    "64c56e77": {
        "name": "ERC20Reentrant",
        "selector": "64c56e77",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"}
                ],
                "name": "AddressEmptyCode",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "AddressInsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {"inputs": [], "name": "FailedInnerCall", "type": "error"},
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "target", "type": "address"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "functionCall",
                "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {
                        "internalType": "enum ERC20Reentrant.Type",
                        "name": "when",
                        "type": "uint8",
                    },
                    {"internalType": "address", "name": "target", "type": "address"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "scheduleReenter",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "functionCall",
            "increaseAllowance",
            "name",
            "scheduleReenter",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "d73f4e3a": {
        "name": "IERC1155MetadataURI",
        "selector": "d73f4e3a",
        "abi": [
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
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
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"}
                ],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "isApprovedForAll",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "uri",
        ],
    },
    "580cf8f5": {
        "name": "ERC721PausableMock",
        "selector": "580cf8f5",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "exists",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
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
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "bytes", "name": "_data", "type": "bytes"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeMint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "unpause",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "burn",
            "exists",
            "getApproved",
            "isApprovedForAll",
            "mint",
            "name",
            "ownerOf",
            "pause",
            "paused",
            "safeMint",
            "safeMint",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
            "unpause",
        ],
    },
    "d57681f2": {
        "name": "ERC1155SupplyMock",
        "selector": "d57681f2",
        "abi": [
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                ],
                "name": "burnBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"}
                ],
                "name": "exists",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mintBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [
                    {"internalType": "string", "name": "newuri", "type": "string"}
                ],
                "name": "setURI",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"}
                ],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "burn",
            "burnBatch",
            "exists",
            "isApprovedForAll",
            "mint",
            "mintBatch",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "setURI",
            "totalSupply",
            "uri",
        ],
    },
    "f47afbe3": {
        "name": "ERC1155URIStorageMock",
        "selector": "f47afbe3",
        "abi": [
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
                    {
                        "internalType": "address[]",
                        "name": "accounts",
                        "type": "address[]",
                    },
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                ],
                "name": "balanceOfBatch",
                "outputs": [
                    {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                ],
                "name": "burnBatch",
                "outputs": [],
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
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "id", "type": "uint256"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "values",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "name": "mintBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
                    {
                        "internalType": "uint256[]",
                        "name": "amounts",
                        "type": "uint256[]",
                    },
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
                "inputs": [
                    {"internalType": "string", "name": "baseURI", "type": "string"}
                ],
                "name": "setBaseURI",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "string", "name": "newuri", "type": "string"}
                ],
                "name": "setURI",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "string", "name": "_tokenURI", "type": "string"},
                ],
                "name": "setURI",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "balanceOf",
            "balanceOfBatch",
            "burn",
            "burnBatch",
            "isApprovedForAll",
            "mint",
            "mintBatch",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "setBaseURI",
            "setURI",
            "setURI",
            "uri",
        ],
    },
    "dbf24b52": {
        "name": "ERC721",
        "selector": "dbf24b52",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC721IncorrectOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "ERC721InsufficientApproval",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC721InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "operator", "type": "address"}
                ],
                "name": "ERC721InvalidOperator",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "ERC721InvalidOwner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC721InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC721InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ERC721NonexistentToken",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "approved",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
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
                        "indexed": True,
                        "internalType": "uint256",
                        "name": "tokenId",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "getApproved",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "operator", "type": "address"},
                ],
                "name": "isApprovedForAll",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
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
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "ownerOf",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
                "inputs": [],
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "approve",
            "balanceOf",
            "getApproved",
            "isApprovedForAll",
            "name",
            "ownerOf",
            "safeTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll",
            "symbol",
            "tokenURI",
            "transferFrom",
        ],
    },
    "3273d15c": {
        "name": "ERC20Burnable",
        "selector": "3273d15c",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "burn",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "burnFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "name": "symbol",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "allowance",
            "approve",
            "balanceOf",
            "burn",
            "burnFrom",
            "decimals",
            "decreaseAllowance",
            "increaseAllowance",
            "name",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
    "aa4b5d98": {
        "name": "ERC165CheckerMock",
        "selector": "aa4b5d98",
        "abi": [
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "bytes4[]",
                        "name": "interfaceIds",
                        "type": "bytes4[]",
                    },
                ],
                "name": "getSupportedInterfaces",
                "outputs": [{"internalType": "bool[]", "name": "", "type": "bool[]"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "bytes4[]",
                        "name": "interfaceIds",
                        "type": "bytes4[]",
                    },
                ],
                "name": "supportsAllInterfaces",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "supportsERC165",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"},
                ],
                "name": "supportsERC165InterfaceUnchecked",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
        ],
        "functions_names": [
            "getSupportedInterfaces",
            "supportsAllInterfaces",
            "supportsERC165",
            "supportsERC165InterfaceUnchecked",
        ],
    },
    "01ffc9a7": {
        "name": "IERC165",
        "selector": "01ffc9a7",
        "abi": [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            }
        ],
        "functions_names": ["supportsInterface"],
    },
    "10163410": {
        "name": "ERC20Permit",
        "selector": "10163410",
        "abi": [
            {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
            {
                "inputs": [
                    {"internalType": "uint256", "name": "length", "type": "uint256"}
                ],
                "name": "ECDSAInvalidSignatureLength",
                "type": "error",
            },
            {
                "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
                "name": "ECDSAInvalidSignatureS",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentAllowance",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "ERC20FailedDecreaseAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "allowance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientAllowance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {"internalType": "uint256", "name": "needed", "type": "uint256"},
                ],
                "name": "ERC20InsufficientBalance",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "approver", "type": "address"}
                ],
                "name": "ERC20InvalidApprover",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "receiver", "type": "address"}
                ],
                "name": "ERC20InvalidReceiver",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "sender", "type": "address"}
                ],
                "name": "ERC20InvalidSender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"}
                ],
                "name": "ERC20InvalidSpender",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"}
                ],
                "name": "ERC2612ExpiredSignature",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "signer", "type": "address"},
                    {"internalType": "address", "name": "owner", "type": "address"},
                ],
                "name": "ERC2612InvalidSigner",
                "type": "error",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "currentNonce",
                        "type": "uint256",
                    },
                ],
                "name": "InvalidAccountNonce",
                "type": "error",
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Approval",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [],
                "name": "EIP712DomainChanged",
                "type": "event",
            },
            {
                "anonymous": False,
                "inputs": [
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
                        "name": "value",
                        "type": "uint256",
                    },
                ],
                "name": "Transfer",
                "type": "event",
            },
            {
                "inputs": [],
                "name": "DOMAIN_SEPARATOR",
                "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                ],
                "name": "allowance",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "approve",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "account", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "requestedDecrease",
                        "type": "uint256",
                    },
                ],
                "name": "decreaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [],
                "name": "eip712Domain",
                "outputs": [
                    {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "version", "type": "string"},
                    {"internalType": "uint256", "name": "chainId", "type": "uint256"},
                    {
                        "internalType": "address",
                        "name": "verifyingContract",
                        "type": "address",
                    },
                    {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
                    {
                        "internalType": "uint256[]",
                        "name": "extensions",
                        "type": "uint256[]",
                    },
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256",
                    },
                ],
                "name": "increaseAllowance",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
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
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
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
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ],
        "functions_names": [
            "DOMAIN_SEPARATOR",
            "allowance",
            "approve",
            "balanceOf",
            "decimals",
            "decreaseAllowance",
            "eip712Domain",
            "increaseAllowance",
            "name",
            "nonces",
            "permit",
            "symbol",
            "totalSupply",
            "transfer",
            "transferFrom",
        ],
    },
}
