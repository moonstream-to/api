from .db import yield_db_session, yield_db_session_ctx
from .models import (
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    PolygonBlock,
    PolygonLabel,
    PolygonTransaction,
    MumbaiBlock,
    MumbaiLabel,
    MumbaiTransaction,
    XDaiBlock,
    XDaiLabel,
    XDaiTransaction,
    WyrmBlock,
    WyrmLabel,
    WyrmTransaction,
)

from enum import Enum

from typing import Type, Union


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    MUMBAI = "mumbai"
    XDAI = "xdai"
    WYRM = "wyrm"


def get_block_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumBlock, PolygonBlock, MumbaiBlock, XDaiBlock, WyrmBlock]]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm
    set proper blocks model.
    """
    block_model: Type[
        Union[EthereumBlock, PolygonBlock, MumbaiBlock, XDaiBlock, WyrmBlock]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        block_model = EthereumBlock
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        block_model = PolygonBlock
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        block_model = MumbaiBlock
    elif blockchain_type == AvailableBlockchainType.XDAI:
        block_model = XDaiBlock
    elif blockchain_type == AvailableBlockchainType.WYRM:
        block_model = WyrmBlock
    else:
        raise Exception("Unsupported blockchain type provided")

    return block_model


def get_label_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumLabel, PolygonLabel, MumbaiLabel, XDaiLabel, WyrmLabel]]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm
    set proper block label model.
    """
    label_model: Type[
        Union[EthereumLabel, PolygonLabel, MumbaiLabel, XDaiLabel, WyrmLabel]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        label_model = EthereumLabel
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        label_model = PolygonLabel
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        label_model = MumbaiLabel
    elif blockchain_type == AvailableBlockchainType.XDAI:
        label_model = XDaiLabel
    elif blockchain_type == AvailableBlockchainType.WYRM:
        label_model = WyrmLabel
    else:
        raise Exception("Unsupported blockchain type provided")

    return label_model


def get_transaction_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[
    Union[
        EthereumTransaction,
        PolygonTransaction,
        MumbaiTransaction,
        XDaiTransaction,
        WyrmTransaction,
    ]
]:
    """
    Depends on provided blockchain type: Ethereum, Polygon, Mumbai, XDai, Wyrm
    set proper block transactions model.
    """
    transaction_model: Type[
        Union[
            EthereumTransaction,
            PolygonTransaction,
            MumbaiTransaction,
            XDaiTransaction,
            WyrmTransaction,
        ]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        transaction_model = EthereumTransaction
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        transaction_model = PolygonTransaction
    elif blockchain_type == AvailableBlockchainType.MUMBAI:
        transaction_model = MumbaiTransaction
    elif blockchain_type == AvailableBlockchainType.XDAI:
        transaction_model = XDaiTransaction
    elif blockchain_type == AvailableBlockchainType.WYRM:
        transaction_model = WyrmTransaction
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
