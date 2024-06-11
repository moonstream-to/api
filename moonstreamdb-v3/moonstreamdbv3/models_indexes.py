import uuid

from sqlalchemy import (
    VARCHAR,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    MetaData,
    PrimaryKeyConstraint,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
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


class utcnow(expression.FunctionElement):
    type = DateTime  # type: ignore


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kwargs):
    return "TIMEZONE('utc', statement_timestamp())"


class EvmBasedBlocks(Base):
    __abstract__ = True

    block_number = Column(BigInteger, primary_key=True, nullable=False, index=True)
    block_hash = Column(VARCHAR(256), nullable=False, index=False)
    block_timestamp = Column(BigInteger, nullable=False, index=True)
    parent_hash = Column(VARCHAR(256), nullable=False)
    row_id = Column(BigInteger, nullable=False, index=False)
    path = Column(Text, nullable=False)
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EvmBasedTransactions(Base):
    __abstract__ = True

    hash = Column(
        VARCHAR(256), primary_key=True, unique=True, nullable=False, index=True
    )
    from_address = Column(LargeBinary(length=20), nullable=False, index=True)
    to_address = Column(LargeBinary(length=20), nullable=False, index=True)
    selector = Column(VARCHAR(256), nullable=True, index=True)
    type = Column(Integer, nullable=True, index=True)
    row_id = Column(BigInteger, nullable=False, index=False)
    block_hash = Column(VARCHAR(256), nullable=False, index=True)
    index = Column(BigInteger, nullable=False, index=True)
    path = Column(Text, nullable=False)
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EvmBasedLogs(Base):
    __abstract__ = True

    block_hash = Column(VARCHAR(256), nullable=False, index=True)
    address = Column(LargeBinary(length=20), nullable=False, index=True)
    row_id = Column(BigInteger, nullable=False, index=False)
    selector = Column(VARCHAR(256), nullable=True, index=False)
    topic1 = Column(VARCHAR(256), nullable=True, index=False)
    topic2 = Column(VARCHAR(256), nullable=True, index=False)
    log_index = Column(BigInteger, nullable=False, index=False)
    path = Column(Text, nullable=False)
    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EvmBasedReorgs(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    block_number = Column(BigInteger, nullable=False, index=True)
    block_hash = Column(VARCHAR(256), nullable=False, index=True)


### Ethereum


class EthereumBlockIndex(EvmBasedBlocks):
    __tablename__ = "ethereum_blocks"


class EthereumTransactionIndex(EvmBasedTransactions):
    __tablename__ = "ethereum_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("ethereum_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class EthereumLogIndex(EvmBasedLogs):
    __tablename__ = "ethereum_logs"

    __table_args__ = (
        Index(
            "idx_ethereum_logs_address_selector", "address", "selector", unique=False
        ),
        Index(
            "idx_ethereum_logs_block_hash_log_index",
            "block_hash",
            "log_index",
            unique=True,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_ethereum_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_ethereum_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("ethereum_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class EthereumReorgs(EvmBasedReorgs):
    __tablename__ = "ethereum_reorgs"


### Polygon


class PolygonBlockIndex(EvmBasedBlocks):
    __tablename__ = "polygon_blocks"


class PolygonTransactionIndex(EvmBasedTransactions):
    __tablename__ = "polygon_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("polygon_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class PolygonLogIndex(EvmBasedLogs):

    __tablename__ = "polygon_logs"

    __table_args__ = (
        Index("idx_polygon_logs_address_selector", "address", "selector", unique=False),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_polygon_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_polygon_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("polygon_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class PolygonReorgs(EvmBasedReorgs):
    __tablename__ = "polygon_reorgs"


### Xai


class XaiBlockIndex(EvmBasedBlocks):
    __tablename__ = "xai_blocks"

    l1_block_number = Column(BigInteger, nullable=False)


class XaiTransactionIndex(EvmBasedTransactions):
    __tablename__ = "xai_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("xai_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class XaiLogIndex(EvmBasedLogs):

    __tablename__ = "xai_logs"

    __table_args__ = (
        Index("idx_xai_logs_address_selector", "address", "selector", unique=False),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_xai_log_idx_tx_hash_log_idx",
        ),
        PrimaryKeyConstraint("transaction_hash", "log_index", name="pk_xai_log_index"),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("xai_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class XaiReorgs(EvmBasedReorgs):
    __tablename__ = "xai_reorgs"


### Xai Sepolia


class XaiSepoliaBlockIndex(EvmBasedBlocks):
    __tablename__ = "xai_sepolia_blocks"

    l1_block_number = Column(BigInteger, nullable=False)


class XaiSepoliaTransactionIndex(EvmBasedTransactions):
    __tablename__ = "xai_sepolia_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("xai_sepolia_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class XaiSepoliaLogIndex(EvmBasedLogs):

    __tablename__ = "xai_sepolia_logs"

    __table_args__ = (
        Index(
            "idx_xai_sepolia_logs_address_selector", "address", "selector", unique=False
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_xai_sepolia_log_idx_tx_hash_log_idx",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_xai_sepolia_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("xai_sepolia_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class XaiSepoliaReorgs(EvmBasedReorgs):
    __tablename__ = "xai_sepolia_reorgs"


### Arbitrum One


class ArbitrumOneBlockIndex(EvmBasedBlocks):
    __tablename__ = "arbitrum_one_blocks"

    l1_block_number = Column(BigInteger, nullable=False)


class ArbitrumOneTransactionIndex(EvmBasedTransactions):
    __tablename__ = "arbitrum_one_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("arbitrum_one_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ArbitrumOneLogIndex(EvmBasedLogs):

    __tablename__ = "arbitrum_one_logs"

    __table_args__ = (
        Index(
            "idx_arbitrum_one_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_arbitrum_one_log_idx_tx_hash_log_idx",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_arbitrum_one_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("arbitrum_one_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ArbitrumOneReorgs(EvmBasedReorgs):
    __tablename__ = "arbitrum_one_reorgs"


### Arbitrum Sepolia


class ArbitrumSepoliaBlockIndex(EvmBasedBlocks):
    __tablename__ = "arbitrum_sepolia_blocks"

    l1_block_number = Column(BigInteger, nullable=False)


class ArbitrumSepoliaTransactionIndex(EvmBasedTransactions):
    __tablename__ = "arbitrum_sepolia_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("arbitrum_sepolia_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ArbitrumSepoliaLogIndex(EvmBasedLogs):

    __tablename__ = "arbitrum_sepolia_logs"

    __table_args__ = (
        Index(
            "idx_arbitrum_sepolia_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_arbitrum_sepolia_log_idx_tx_hash_log_idx",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_arbitrum_sepolia_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("arbitrum_sepolia_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ArbitrumSepoliaReorgs(EvmBasedReorgs):
    __tablename__ = "arbitrum_sepolia_reorgs"


### Game7 Orbit Arbitrum Sepolia


class Game7OrbitArbitrumSepoliaBlockIndex(EvmBasedBlocks):
    __tablename__ = "game7_orbit_arbitrum_sepolia_blocks"

    l1_block_number = Column(BigInteger, nullable=False)


class Game7OrbitArbitrumSepoliaTransactionIndex(EvmBasedTransactions):
    __tablename__ = "game7_orbit_arbitrum_sepolia_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey(
            "game7_orbit_arbitrum_sepolia_blocks.block_number", ondelete="CASCADE"
        ),
        nullable=False,
        index=True,
    )


class Game7OrbitArbitrumSepoliaLogIndex(EvmBasedLogs):

    __tablename__ = "game7_orbit_arbitrum_sepolia_logs"

    __table_args__ = (
        Index(
            "idx_game7_orbit_arbitrum_sepolia_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_g7o_arbitrum_sepolia_log_idx_tx_hash_log_idx",
        ),
        PrimaryKeyConstraint(
            "transaction_hash",
            "log_index",
            name="pk_game7_orbit_arbitrum_sepolia_log_index",
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey(
            "game7_orbit_arbitrum_sepolia_transactions.hash", ondelete="CASCADE"
        ),
        nullable=False,
        index=True,
    )


class Game7OrbitArbitrumSepoliaReorgs(EvmBasedReorgs):
    __tablename__ = "game7_orbit_arbitrum_sepolia_reorgs"


### Mantle


class MantleBlockIndex(EvmBasedBlocks):
    __tablename__ = "mantle_blocks"


class MantleTransactionIndex(EvmBasedTransactions):
    __tablename__ = "mantle_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("mantle_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class MantleLogIndex(EvmBasedLogs):
    __tablename__ = "mantle_logs"

    __table_args__ = (
        Index("idx_mantle_logs_address_selector", "address", "selector", unique=False),
        Index(
            "idx_mantle_logs_block_hash_log_index",
            "block_hash",
            "log_index",
            unique=True,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_mantle_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_mantle_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("mantle_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class MantleReorgs(EvmBasedReorgs):
    __tablename__ = "mantle_reorgs"


### Mantle Sepolia


class MantleSepoliaBlockIndex(EvmBasedBlocks):
    __tablename__ = "mantle_sepolia_blocks"


class MantleSepoliaTransactionIndex(EvmBasedTransactions):
    __tablename__ = "mantle_sepolia_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("mantle_sepolia_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class MantleSepoliaLogIndex(EvmBasedLogs):
    __tablename__ = "mantle_sepolia_logs"

    __table_args__ = (
        Index(
            "idx_mantle_sepolia_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        Index(
            "idx_mantle_sepolia_logs_block_hash_log_index",
            "block_hash",
            "log_index",
            unique=True,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_mantle_sepolia_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_mantle_sepolia_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("mantle_sepolia_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class MantleSepoliaReorgs(EvmBasedReorgs):
    __tablename__ = "mantle_sepolia_reorgs"


### ABI Jobs


class AbiJobs(Base):
    __tablename__ = "abi_jobs"

    __table_args__ = (
        UniqueConstraint(
            "chain", "address", "abi_selector", "customer_id", name="uq_abi_jobs"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = Column(LargeBinary, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    abi_selector = Column(VARCHAR(256), nullable=False, index=True)
    chain = Column(VARCHAR(256), nullable=False, index=True)
    abi_name = Column(VARCHAR(256), nullable=False, index=True)
    status = Column(VARCHAR(256), nullable=False, index=True)
    historical_crawl_status = Column(VARCHAR(256), nullable=False, index=True)
    progress = Column(Integer, nullable=False, index=False)
    moonworm_task_pickedup = Column(Boolean, nullable=False, index=False)
    abi = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
