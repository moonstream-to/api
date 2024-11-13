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

import os
import uuid

from sqlalchemy import (
    VARCHAR,
    BigInteger,
    Column,
    DateTime,
    Index,
    Integer,
    LargeBinary,
    MetaData,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression, text

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

MOONSTREAM_DB_V3_SCHEMA_NAME = os.environ.get(
    "MOONSTREAM_DB_V3_SCHEMA_NAME", "blockchain"
)


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
        LargeBinary,
        nullable=True,
        index=True,
    )
    origin_address = Column(
        LargeBinary,
        nullable=True,
        index=True,
    )

    address = Column(
        LargeBinary,
        nullable=False,
        index=True,
    )

    label_name = Column(Text, nullable=True, index=True)
    label_type = Column(VARCHAR(64), nullable=True, index=True)
    label_data = Column(JSONB, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EvmBasedTransaction(Base):  # type: ignore
    __abstract__ = True

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    block_number = (
        Column(
            BigInteger,
            nullable=False,
            index=True,
        ),
    )
    block_timestamp = Column(BigInteger, nullable=False, index=True)
    block_hash = Column(VARCHAR(256), nullable=False, index=True)
    from_address = Column(LargeBinary, index=True)
    to_address = Column(LargeBinary, index=True)
    gas = Column(BigInteger, index=True)
    gas_price = Column(BigInteger, index=True)
    max_fee_per_gas = Column(BigInteger, nullable=True)
    max_priority_fee_per_gas = Column(BigInteger, nullable=True)
    input = Column(Text)
    nonce = Column(BigInteger)
    transaction_index = Column(BigInteger)
    transaction_type = Column(Integer, nullable=True)
    value = Column(BigInteger, index=True)

    indexed_at = Column(
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
        Index(
            "uk_ethereum_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_ethereum_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_ethereum_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_ethereum_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class EthereumTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "ethereum_transactions"


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
        Index(
            "uk_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class SepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "sepolia_transactions"


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
        Index(
            "uk_polygon_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_polygon_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_polygon_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_polygon_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class PolygonTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "polygon_transactions"


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
        Index(
            "uk_mumbai_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_mumbai_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_mumbai_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_mumbai_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class MumbaiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "mumbai_transactions"


class AmoyLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "amoy_labels"

    __table_args__ = (
        Index(
            "ix_amoy_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_amoy_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_amoy_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_amoy_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_amoy_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_amoy_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class AmoyTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "amoy_transactions"


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
        Index(
            "uk_xdai_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_xdai_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_xdai_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_xdai_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class XDaiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "xdai_transactions"


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
        Index(
            "uk_zksync_era_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_zksync_era_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_zksync_era_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_zksync_era_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ZkSyncEraTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "zksync_era_transactions"


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
        Index(
            "uk_zksync_era_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_zksync_era_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_zksync_era_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_zksync_era_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ZkSyncEraSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "zksync_era_sepolia_transactions"


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
        Index(
            "uk_base_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_base_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_base_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_base_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class BaseTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "base_transactions"


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
        Index(
            "uk_arbitrum_nova_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_arbitrum_nova_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_arbitrum_nova_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_arbitrum_nova_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ArbitrumNovaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "arbitrum_nova_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


class ArbitrumOneLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "arbitrum_one_labels"

    __table_args__ = (
        Index(
            "ix_arbitrum_one_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_arbitrum_one_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_arbitrum_one_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_arbitrum_one_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_arbitrum_one_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_arbitrum_one_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ArbitrumOneTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "arbitrum_one_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


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
        Index(
            "uk_arbitrum_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_arbitrum_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_arbitrum_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_arbitrum_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ArbitrumSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "arbitrum_sepolia_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


class Game7OrbitArbitrumSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "game7_orbit_arbitrum_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_g7o_arbitrum_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_g7o_arbitrum_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_g7o_arbitrum_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_g7o_arbitrum_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_g7o_arbitrum_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_g7o_arbitrum_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class Game7OrbitArbitrumSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "game7_orbit_arbitrum_sepolia_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


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
        Index(
            "uk_xai_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_xai_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_xai_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_xai_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class XaiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "xai_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


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
        Index(
            "uk_xai_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_xai_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_xai_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_xai_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class XaiSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "xai_sepolia_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


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
        Index(
            "uk_avalanche_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_avalanche_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_avalanche_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_avalanche_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class AvalancheTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "avalanche_transactions"


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
        Index(
            "uk_avalanche_fuji_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_avalanche_fuji_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_avalanche_fuji_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_avalanche_fuji_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class AvalancheFujiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "avalanche_fuji_transactions"


class BlastLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "blast_labels"

    __table_args__ = (
        Index(
            "ix_blast_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_blast_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_blast_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_blast_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_blast_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_blast_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class BlastTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "blast_transactions"


class BlastSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "blast_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_blast_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_blast_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_blast_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_blast_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_blast_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_blast_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class BlastSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "blast_sepolia_transactions"


class ProofOfPlayApexLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "proofofplay_apex_labels"

    __table_args__ = (
        Index(
            "ix_proofofplay_apex_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_proofofplay_apex_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_proofofplay_apex_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_proofofplay_apex_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_proofofplay_apex_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_proofofplay_apex_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ProofOfPlayApexTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "proofofplay_apex_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


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
        Index(
            "uk_starknet_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_starknet_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_starknet_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_starknet_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
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
        Index(
            "uk_starknet_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_starknet_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_starknet_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_starknet_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class MantleLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "mantle_labels"

    __table_args__ = (
        Index(
            "ix_mantle_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_mantle_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_mantle_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_mantle_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_mantle_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_mantle_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class MantleTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "mantle_transactions"


class MantleSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "mantle_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_mantle_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_mantle_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_mantle_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_mantle_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_mantle_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_mantle_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class MantleSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "mantle_sepolia_transactions"


class ImxZkevmLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "imx_zkevm_labels"

    __table_args__ = (
        Index(
            "ix_imx_zkevm_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_imx_zkevm_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_imx_zkevm_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_imx_zkevm_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_imx_zkevm_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_imx_zkevm_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ImxZkevmTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "imx_zkevm_transactions"


class ImxZkevmSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "imx_zkevm_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_imx_zkevm_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_imx_zkevm_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_imx_zkevm_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_imx_zkevm_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_imx_zkevm_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_imx_zkevm_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class ImxZkevmSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "imx_zkevm_sepolia_transactions"


class Game7Label(EvmBasedLabel):  # type: ignore
    __tablename__ = "game7_labels"

    __table_args__ = (
        Index(
            "ix_game7_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_game7_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_game7_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_game7_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_game7_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_game7_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class Game7Transaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "game7_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


class Game7TestnetLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "game7_testnet_labels"

    __table_args__ = (
        Index(
            "ix_game7_testnet_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_game7_testnet_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_game7_testnet_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_game7_testnet_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_game7_testnet_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_game7_testnet_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class Game7TestnetTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "game7_testnet_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


class B3Label(EvmBasedLabel):  # type: ignore
    __tablename__ = "b3_labels"

    __table_args__ = (
        Index(
            "ix_b3_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_b3_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_b3_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_b3_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_b3_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_b3_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class B3Transaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "b3_transactions"


class B3SepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "b3_sepolia_labels"

    __table_args__ = (
        Index(
            "ix_b3_sepolia_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_b3_sepolia_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_b3_sepolia_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_b3_sepolia_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_b3_sepolia_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_b3_sepolia_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class B3SepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "b3_sepolia_transactions"


class RoninLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "ronin_labels"

    __table_args__ = (
        Index(
            "ix_ronin_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_ronin_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_ronin_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_ronin_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_ronin_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_ronin_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class RoninSaigonLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "ronin_saigon_labels"

    __table_args__ = (
        Index(
            "ix_ronin_saigon_labels_addr_block_num",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_ronin_saigon_labels_addr_block_ts",
            "address",
            "block_timestamp",
            unique=False,
        ),
        Index(
            "uk_ronin_saigon_labels_tx_hash_tx_call",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer' and label_type='tx_call'"),
        ),
        Index(
            "uk_ronin_saigon_labels_tx_hash_log_idx_evt",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer' and label_type='event'"),
        ),
        Index(
            "uk_ronin_saigon_labels_tx_hash_tx_call_raw",
            "transaction_hash",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='tx_call'"),
        ),
        Index(
            "uk_ronin_saigon_labels_tx_hash_log_idx_evt_raw",
            "transaction_hash",
            "log_index",
            unique=True,
            postgresql_where=text("label='seer-raw' and label_type='event'"),
        ),
    )


class RoninTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "ronin_transactions"
