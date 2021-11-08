from dataclasses import dataclass
from typing import Optional


@dataclass
class ContractDeployment:
    address: str
    block_number: int
    transaction_hash: str
    deployer_address: str
    block_timestamp: int
    gas_used: int
    gas_price: int
    transaction_fee: int


@dataclass
class BlockBounds:
    starting_block: int
    ending_block: Optional[int] = None
