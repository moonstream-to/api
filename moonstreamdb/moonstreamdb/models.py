import uuid

from sqlalchemy import (
    VARCHAR,
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression

"""
Naming conventions doc
https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
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


class EthereumBlock(Base):  # type: ignore
    __tablename__ = "ethereum_blocks"

    block_number = Column(
        BigInteger, primary_key=True, unique=True, nullable=False, index=True
    )
    difficulty = Column(BigInteger)
    extra_data = Column(VARCHAR(128))
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    base_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    hash = Column(VARCHAR(256), index=True)
    logs_bloom = Column(VARCHAR(1024))
    miner = Column(VARCHAR(256))
    nonce = Column(VARCHAR(256))
    parent_hash = Column(VARCHAR(256))
    receipt_root = Column(VARCHAR(256))
    uncles = Column(VARCHAR(256))
    size = Column(Integer)
    state_root = Column(VARCHAR(256))
    timestamp = Column(BigInteger, index=True)
    total_difficulty = Column(VARCHAR(256))
    transactions_root = Column(VARCHAR(256))
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EthereumTransaction(Base):  # type: ignore
    __tablename__ = "ethereum_transactions"

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    block_number = Column(
        BigInteger,
        ForeignKey("ethereum_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Numeric(precision=78, scale=0), index=True)
    gas_price = Column(Numeric(precision=78, scale=0), index=True)
    max_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    max_priority_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    transaction_type = Column(Integer, nullable=True)
    value = Column(Numeric(precision=78, scale=0), index=True)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EthereumLabel(Base):  # type: ignore
    """
    Example of label_data:
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

    __tablename__ = "ethereum_labels"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    label = Column(VARCHAR(256), nullable=False, index=True)
    block_number = Column(
        BigInteger,
        nullable=True,
        index=True,
    )
    address = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    transaction_hash = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    label_data = Column(JSONB, nullable=True)
    block_timestamp = Column(BigInteger, index=True)
    log_index = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class PolygonBlock(Base):  # type: ignore
    __tablename__ = "polygon_blocks"

    block_number = Column(
        BigInteger, primary_key=True, unique=True, nullable=False, index=True
    )
    difficulty = Column(BigInteger)
    extra_data = Column(VARCHAR(128))
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    base_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    hash = Column(VARCHAR(256), index=True)
    logs_bloom = Column(VARCHAR(1024))
    miner = Column(VARCHAR(256))
    nonce = Column(VARCHAR(256))
    parent_hash = Column(VARCHAR(256))
    receipt_root = Column(VARCHAR(256))
    uncles = Column(VARCHAR(256))
    size = Column(Integer)
    state_root = Column(VARCHAR(256))
    timestamp = Column(BigInteger, index=True)
    total_difficulty = Column(VARCHAR(256))
    transactions_root = Column(VARCHAR(256))
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class PolygonTransaction(Base):  # type: ignore
    __tablename__ = "polygon_transactions"

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    block_number = Column(
        BigInteger,
        ForeignKey("polygon_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Numeric(precision=78, scale=0), index=True)
    gas_price = Column(Numeric(precision=78, scale=0), index=True)
    max_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    max_priority_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    transaction_type = Column(Integer, nullable=True)
    value = Column(Numeric(precision=78, scale=0), index=True)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class PolygonLabel(Base):  # type: ignore
    """
    Example of label_data:
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

    __tablename__ = "polygon_labels"

    __table_args__ = (
        Index(
            "ix_polygon_labels_address_block_number",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_polygon_labels_address_block_timestamp",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    label = Column(VARCHAR(256), nullable=False, index=True)
    block_number = Column(
        BigInteger,
        nullable=True,
        index=True,
    )
    address = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    transaction_hash = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    label_data = Column(JSONB, nullable=True)
    block_timestamp = Column(BigInteger, index=True)
    log_index = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class MumbaiBlock(Base):  # type: ignore
    __tablename__ = "mumbai_blocks"

    block_number = Column(
        BigInteger, primary_key=True, unique=True, nullable=False, index=True
    )
    difficulty = Column(BigInteger)
    extra_data = Column(VARCHAR(128))
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    base_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    hash = Column(VARCHAR(256), index=True)
    logs_bloom = Column(VARCHAR(1024))
    miner = Column(VARCHAR(256))
    nonce = Column(VARCHAR(256))
    parent_hash = Column(VARCHAR(256))
    receipt_root = Column(VARCHAR(256))
    uncles = Column(VARCHAR(256))
    size = Column(Integer)
    state_root = Column(VARCHAR(256))
    timestamp = Column(BigInteger, index=True)
    total_difficulty = Column(VARCHAR(256))
    transactions_root = Column(VARCHAR(256))
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class MumbaiTransaction(Base):  # type: ignore
    __tablename__ = "mumbai_transactions"

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    block_number = Column(
        BigInteger,
        ForeignKey("mumbai_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Numeric(precision=78, scale=0), index=True)
    gas_price = Column(Numeric(precision=78, scale=0), index=True)
    max_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    max_priority_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    transaction_type = Column(Integer, nullable=True)
    value = Column(Numeric(precision=78, scale=0), index=True)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class MumbaiLabel(Base):  # type: ignore
    __tablename__ = "mumbai_labels"

    __table_args__ = (
        Index(
            "ix_mumbai_labels_address_block_number",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_mumbai_labels_address_block_timestamp",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    label = Column(VARCHAR(256), nullable=False, index=True)
    block_number = Column(
        BigInteger,
        nullable=True,
        index=True,
    )
    address = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    transaction_hash = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    label_data = Column(JSONB, nullable=True)
    block_timestamp = Column(BigInteger, index=True)
    log_index = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class XDaiBlock(Base):  # type: ignore
    __tablename__ = "xdai_blocks"

    author = Column(VARCHAR(128))
    block_number = Column(
        BigInteger, primary_key=True, unique=True, nullable=False, index=True
    )
    difficulty = Column(VARCHAR(128))
    extra_data = Column(VARCHAR(128))
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    base_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    hash = Column(VARCHAR(256), index=True)
    logs_bloom = Column(VARCHAR(1024))
    miner = Column(VARCHAR(256))
    nonce = Column(VARCHAR(256), nullable=True)
    parent_hash = Column(VARCHAR(256))
    receipt_root = Column(VARCHAR(256))
    uncles = Column(VARCHAR(256))
    signature = Column(VARCHAR(256))
    size = Column(Integer)
    state_root = Column(VARCHAR(256))
    step = Column(BigInteger)
    timestamp = Column(BigInteger, index=True)
    total_difficulty = Column(VARCHAR(256))
    transactions_root = Column(VARCHAR(256))
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class XDaiTransaction(Base):  # type: ignore
    __tablename__ = "xdai_transactions"

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    block_number = Column(
        BigInteger,
        ForeignKey("xdai_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    data = Column(Text)
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Numeric(precision=78, scale=0), index=True)
    gas_price = Column(Numeric(precision=78, scale=0), index=True)
    max_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    max_priority_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    transaction_type = Column(Integer, nullable=True)
    value = Column(Numeric(precision=78, scale=0), index=True)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class XDaiLabel(Base):  # type: ignore
    """
    Example of label_data:
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

    __tablename__ = "xdai_labels"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    label = Column(VARCHAR(256), nullable=False, index=True)
    block_number = Column(
        BigInteger,
        nullable=True,
        index=True,
    )
    address = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    transaction_hash = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    label_data = Column(JSONB, nullable=True)
    block_timestamp = Column(BigInteger, index=True)
    log_index = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class WyrmBlock(Base):  # type: ignore
    __tablename__ = "wyrm_blocks"

    block_number = Column(
        BigInteger, primary_key=True, unique=True, nullable=False, index=True
    )
    difficulty = Column(BigInteger)
    extra_data = Column(VARCHAR(128))
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    base_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    hash = Column(VARCHAR(256), index=True)
    logs_bloom = Column(VARCHAR(1024))
    miner = Column(VARCHAR(256))
    nonce = Column(VARCHAR(256))
    parent_hash = Column(VARCHAR(256))
    receipt_root = Column(VARCHAR(256))
    uncles = Column(VARCHAR(256))
    size = Column(Integer)
    state_root = Column(VARCHAR(256))
    timestamp = Column(BigInteger, index=True)
    total_difficulty = Column(VARCHAR(256))
    transactions_root = Column(VARCHAR(256))
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class WyrmTransaction(Base):  # type: ignore
    __tablename__ = "wyrm_transactions"

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    block_number = Column(
        BigInteger,
        ForeignKey("wyrm_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Numeric(precision=78, scale=0), index=True)
    gas_price = Column(Numeric(precision=78, scale=0), index=True)
    max_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    max_priority_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    transaction_type = Column(Integer, nullable=True)
    value = Column(Numeric(precision=78, scale=0), index=True)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class WyrmLabel(Base):  # type: ignore
    """
    Example of label_data:
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

    __tablename__ = "wyrm_labels"

    __table_args__ = (
        Index(
            "ix_wyrm_labels_address_block_number",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_wyrm_labels_address_block_timestamp",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    label = Column(VARCHAR(256), nullable=False, index=True)
    block_number = Column(
        BigInteger,
        nullable=True,
        index=True,
    )
    address = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    transaction_hash = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    label_data = Column(JSONB, nullable=True)
    block_timestamp = Column(BigInteger, index=True)
    log_index = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class ZkSyncEraTestnetBlock(Base):  # type: ignore
    __tablename__ = "zksync_era_testnet_blocks"

    block_number = Column(
        BigInteger, primary_key=True, unique=True, nullable=False, index=True
    )
    difficulty = Column(BigInteger)
    extra_data = Column(VARCHAR(128))
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    base_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    hash = Column(VARCHAR(256), index=True)
    logs_bloom = Column(VARCHAR(1024))
    miner = Column(VARCHAR(256))
    nonce = Column(VARCHAR(256))
    parent_hash = Column(VARCHAR(256))
    receipt_root = Column(VARCHAR(256))
    uncles = Column(VARCHAR(256))
    size = Column(Integer)
    state_root = Column(VARCHAR(256))
    timestamp = Column(BigInteger, index=True)
    total_difficulty = Column(VARCHAR(256))
    transactions_root = Column(VARCHAR(256))

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )

    mix_hash = Column(VARCHAR(256), nullable=True)
    sha3_uncles = Column(VARCHAR(256), nullable=True)

    l1_batch_number = Column(BigInteger, nullable=True)
    l1_batch_timestamp = Column(BigInteger, nullable=True)


class ZkSyncEraTestnetTransaction(Base):  # type: ignore
    __tablename__ = "zksync_era_testnet_transactions"

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    block_number = Column(
        BigInteger,
        ForeignKey("zksync_era_testnet_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Numeric(precision=78, scale=0), index=True)
    gas_price = Column(Numeric(precision=78, scale=0), index=True)
    max_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    max_priority_fee_per_gas = Column(Numeric(precision=78, scale=0), nullable=True)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    transaction_type = Column(Integer, nullable=True)
    value = Column(Numeric(precision=78, scale=0), index=True)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )

    l1_batch_number = Column(BigInteger, nullable=True)
    l1_batch_tx_index = Column(BigInteger, nullable=True)


class ZkSyncEraTestnetLabel(Base):  # type: ignore
    """
    Example of label_data:
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

    __tablename__ = "zksync_era_testnet_labels"

    __table_args__ = (
        Index(
            "ix_zksync_era_testnet_labels_address_block_number",
            "address",
            "block_number",
            unique=False,
        ),
        Index(
            "ix_zksync_era_testnet_labels_address_block_timestamp",
            "address",
            "block_timestamp",
            unique=False,
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    label = Column(VARCHAR(256), nullable=False, index=True)
    block_number = Column(
        BigInteger,
        nullable=True,
        index=True,
    )
    address = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    transaction_hash = Column(
        VARCHAR(256),
        nullable=True,
        index=True,
    )
    label_data = Column(JSONB, nullable=True)
    block_timestamp = Column(BigInteger, index=True)
    log_index = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class ESDFunctionSignature(Base):  # type: ignore
    """
    Function signature from blockchain (Ethereum/Polygon) Signature Database.
    """

    __tablename__ = "esd_function_signatures"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, index=True)
    text_signature = Column(Text, nullable=False)
    hex_signature = Column(VARCHAR(10), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class ESDEventSignature(Base):  # type: ignore
    """
    Function signature from blockchain (Ethereum/Polygon) Signature Database.
    """

    __tablename__ = "esd_event_signatures"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, index=True)
    text_signature = Column(Text, nullable=False)
    hex_signature = Column(VARCHAR(66), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class OpenSeaCrawlingState(Base):  # type: ignore
    """
    Model for control opeansea crawling state.
    """

    __tablename__ = "opensea_crawler_state"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    query = Column(Text, nullable=False)
    crawled_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )

    total_count = Column(Integer, nullable=False)
