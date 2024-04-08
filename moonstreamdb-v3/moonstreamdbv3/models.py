"""
Moonstream database V3

Example of label_data column record:
    {
        "label": "ERC20",
        "label_data": {
            "name": "Uniswap",
            "symbol": "UNI"
        }
    },
    {
        "label": "Exchange"
        "label_data": {...}
    }
"""

import uuid

from sqlalchemy import (
    VARCHAR,
    BigInteger,
    Column,
    DateTime,
    Index,
    Integer,
    MetaData,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression

"""
Naming conventions doc
https://docs.sqlalchemy.org/en/20/core/constraints.html#configuring-constraint-naming-conventions
"""
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

"""
Creating a utcnow function which runs on the Posgres database server when created_at and updated_at
fields are populated.
Following:
1. https://docs.sqlalchemy.org/en/13/core/compiler.html#utc-timestamp-function
2. https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT
3. https://stackoverflow.com/a/33532154/13659585
"""


class utcnow(expression.FunctionElement):
    type = DateTime  # type: ignore


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kwargs):
    return "TIMEZONE('utc', statement_timestamp())"


class EvmBasedLabel(Base):  # type: ignore
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    label = Column(VARCHAR(256), nullable=False, index=True)

    transaction_hash = Column(
        VARCHAR(128),
        nullable=False,
        index=True,
    )
    log_index = Column(Integer, nullable=True)

    block_number = Column(
        BigInteger,
        nullable=False,
        index=True,
    )
    block_hash = Column(VARCHAR(256), nullable=False)
    block_timestamp = Column(BigInteger, nullable=False)

    caller_address = Column(
        VARCHAR(64),
        nullable=True,
        index=True,
    )
    origin_address = Column(
        VARCHAR(64),
        nullable=True,
        index=True,
    )
    address = Column(
        VARCHAR(64),
        nullable=True,
        index=True,
    )

    label_name = Column(Text, nullable=True, index=True)
    label_type = Column(VARCHAR(64), nullable=True, index=True)
    label_data = Column(JSONB, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EthereumLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "ethereum_labels"

    __table_args__ = (
        Index(
            "ix_ethereum_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_ethereum_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class SepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "sepolia_labels"

    __table_args__ = (
        Index(
            "ix_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class PolygonLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "polygon_labels"

    __table_args__ = (
        Index(
            "ix_polygon_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_polygon_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class MumbaiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "mumbai_labels"

    __table_args__ = (
        Index(
            "ix_mumbai_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_mumbai_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class XDaiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "xdai_labels"

    __table_args__ = (
        Index(
            "ix_xdai_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_xdai_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class ZkSyncEraLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "zksync_era_labels"

    __table_args__ = (
        Index(
            "ix_zksync_era_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_zksync_era_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class ZkSyncEraSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "zksync_era_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_zksync_era_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_zksync_era_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class BaseLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "base_labels"

    __table_args__ = (
        Index(
            "ix_base_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_base_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class ArbitrumNovaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "arbitrum_nova_labels"

    __table_args__ = (
        Index(
            "ix_arbitrum_nova_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_arbitrum_nova_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class ArbitrumSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "arbitrum_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_arbitrum_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_arbitrum_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class XaiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "xai_labels"

    __table_args__ = (
        Index(
            "ix_xai_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_xai_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class XaiSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "xai_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_xai_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_xai_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class AvalancheLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "avalanche_labels"

    __table_args__ = (
        Index(
            "ix_avalanche_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_avalanche_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class AvalancheFujiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "avalanche_fuji_labels"

    __table_args__ = (
        Index(
            "ix_avalanche_fuji_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_avalanche_fuji_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class StarknetLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "starknet_labels"

    __table_args__ = (
        Index(
            "ix_starknet_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_starknet_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )


class StarknetSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "starknet_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_starknet_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_starknet_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )
