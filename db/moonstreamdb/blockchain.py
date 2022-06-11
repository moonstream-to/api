from .db import yield_db_session, yield_db_session_ctx
from .models import (
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    PolygonBlock,
    PolygonLabel,
    PolygonTransaction,
    XDaiBlock,
    XDaiLabel,
    XDaiTransaction,
)

from enum import Enum

from typing import Type, Union


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    XDAI = "xdai"


def get_block_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumBlock, PolygonBlock, XDaiBlock]]:
    """
    Depends on provided blockchain type: Ethereum, Polygon or XDai,
    set proper blocks model: EthereumBlock, PolygonBlock or XdaiBlock.
    """
    block_model: Type[Union[EthereumBlock, PolygonBlock, XDaiBlock]]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        block_model = EthereumBlock
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        block_model = PolygonBlock
    elif blockchain_type == AvailableBlockchainType.XDAI:
        block_model = XDaiBlock
    else:
        raise Exception("Unsupported blockchain type provided")

    return block_model


def get_label_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumLabel, PolygonLabel, XDaiLabel]]:
    """
    Depends on provided blockchain type: Ethereum, Polygon or XDai,
    set proper block label model: EthereumLabel, PolygonLabel or XdaiLabel.
    """
    label_model: Type[Union[EthereumLabel, PolygonLabel, XDaiLabel]]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        label_model = EthereumLabel
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        label_model = PolygonLabel
    elif blockchain_type == AvailableBlockchainType.XDAI:
        label_model = XDaiLabel
    else:
        raise Exception("Unsupported blockchain type provided")

    return label_model


def get_transaction_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumTransaction, PolygonTransaction, XDaiTransaction]]:
    """
    Depends on provided blockchain type: Ethereum or Polygon,
    set proper block transactions model: EthereumTransaction or PolygonTransaction.
    """
    transaction_model: Type[
        Union[EthereumTransaction, PolygonTransaction, XDaiTransaction]
    ]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        transaction_model = EthereumTransaction
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        transaction_model = PolygonTransaction
    elif blockchain_type == AvailableBlockchainType.XDAI:
        transaction_model = XDaiTransaction
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
