from .db import yield_db_session, yield_db_session_ctx
from .models import (
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    PolygonBlock,
    PolygonLabel,
    PolygonTransaction,
)

from enum import Enum

from typing import Type, Union


class AvailableBlockchainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"


def get_block_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumBlock, PolygonBlock]]:
    """
    Depends on provided blockchain type: Ethereum or Polygon,
    set proper blocks model: EthereumBlock or PolygonBlock.
    """
    block_model: Type[Union[EthereumBlock, PolygonBlock]]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        block_model = EthereumBlock
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        block_model = PolygonBlock
    else:
        raise Exception("Unsupported blockchain type provided")

    return block_model


def get_label_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumLabel, PolygonLabel]]:
    """
    Depends on provided blockchain type: Ethereum or Polygon,
    set proper block label model: EthereumLabel or PolygonLabel.
    """
    label_model: Type[Union[EthereumLabel, PolygonLabel]]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        label_model = EthereumLabel
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        label_model = PolygonLabel
    else:
        raise Exception("Unsupported blockchain type provided")

    return label_model


def get_transaction_model(
    blockchain_type: AvailableBlockchainType,
) -> Type[Union[EthereumTransaction, PolygonTransaction]]:
    """
    Depends on provided blockchain type: Ethereum or Polygon,
    set proper block transactions model: EthereumTransaction or PolygonTransaction.
    """
    transaction_model: Type[Union[EthereumTransaction, PolygonTransaction]]
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        transaction_model = EthereumTransaction
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        transaction_model = PolygonTransaction
    else:
        raise Exception("Unsupported blockchain type provided")

    return transaction_model
