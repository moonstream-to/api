"""
Data structures used in (and as part of the maintenance of) the Moonstream NFTs dataset
"""
from dataclasses import dataclass
from enum import Enum
from os import name
from typing import Any, Dict, Optional, Union


@dataclass
class BlockBounds:
    starting_block: int
    ending_block: Optional[int] = None


@dataclass
class NftTransaction:
    blockchain_type: str
    block_number: int
    block_timestamp: int
    transaction_hash: str
    contract_address: str
    caller_address: str
    function_name: str
    function_args: Union[Dict[str, Any], str]
    gas_used: int
    gas_price: int
    value: int
    status: int
    max_fee_per_gas: Optional[int] = None
    max_priority_fee_per_gas: Optional[int] = None


@dataclass
class NftApprovalEvent:
    blockchain_type: str
    token_address: str
    owner: str
    approved: str
    token_id: str
    transaction_hash: str
    log_index: int


@dataclass
class NftApprovalForAllEvent:
    blockchain_type: str
    token_address: str
    owner: str
    approved: str
    operator: str
    transaction_hash: str
    log_index: int


@dataclass
class NftTransferEvent:
    blockchain_type: str
    token_address: str
    from_address: str
    to_address: str
    token_id: str
    transaction_hash: str
    log_index: int


@dataclass
class Erc20TransferEvent:
    blockchain_type: str
    token_address: str
    from_address: str
    to_address: str
    value: int
    transaction_hash: str
    log_index: int
