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
from sqlalchemy.dialects.postgresql import UUID, JSONB
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
    transactions_indexed_at = Column(DateTime(timezone=True), nullable=True)
    logs_indexed_at = Column(DateTime(timezone=True), nullable=True)
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
    topic3 = Column(VARCHAR(256), nullable=True, index=False)
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


class evmBasedContracts(Base):
    __abstract__ = True
    address = Column(LargeBinary(length=20), primary_key=True, nullable=False)
    deployed_by = Column(LargeBinary(length=20), nullable=False, index=True)
    deployed_bytecode = Column(Text, nullable=False)
    deployed_bytecode_hash = Column(
        VARCHAR(32), nullable=False, index=True
    )  # MD5 hash of the deployed bytecode
    bytecode_storage_id = Column(
        UUID(as_uuid=True), ForeignKey("bytecode_storage.id"), nullable=True
    )
    abi = Column(JSONB, nullable=True)
    deployed_at_block_number = Column(BigInteger, nullable=False)
    deployed_at_block_hash = Column(VARCHAR(256), nullable=False)
    deployed_at_block_timestamp = Column(BigInteger, nullable=False)
    transaction_hash = Column(VARCHAR(256), nullable=False, index=True)
    transaction_index = Column(BigInteger, nullable=False)
    name = Column(VARCHAR(256), nullable=True, index=True)
    statistics = Column(JSONB, nullable=True)
    supported_standards = Column(JSONB, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )


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


class EthereumContracts(evmBasedContracts):
    __tablename__ = "ethereum_contracts"


### Sepolia


class SepoliaBlockIndex(EvmBasedBlocks):
    __tablename__ = "sepolia_blocks"


class SepoliaTransactionIndex(EvmBasedTransactions):
    __tablename__ = "sepolia_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("sepolia_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class SepoliaLogIndex(EvmBasedLogs):

    __tablename__ = "sepolia_logs"

    __table_args__ = (
        Index(
            "idx_sepolia_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        Index(
            "idx_sepolia_logs_block_hash_log_index",
            "block_hash",
            "log_index",
            unique=True,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_sepolia_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_sepolia_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("sepolia_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class SepoliaReorgs(EvmBasedReorgs):
    __tablename__ = "sepolia_reorgs"


class SepoliaContracts(evmBasedContracts):
    __tablename__ = "sepolia_contracts"


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


class PolygonContracts(evmBasedContracts):
    __tablename__ = "polygon_contracts"


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


class XaiContracts(evmBasedContracts):
    __tablename__ = "xai_contracts"


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


class XaiSepoliaContracts(evmBasedContracts):
    __tablename__ = "xai_sepolia_contracts"


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


class ArbitrumOneContracts(evmBasedContracts):
    __tablename__ = "arbitrum_one_contracts"


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


class ArbitrumSepoliaContracts(evmBasedContracts):
    __tablename__ = "arbitrum_sepolia_contracts"


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


class Game7OrbitArbitrumSepoliaContracts(evmBasedContracts):
    __tablename__ = "game7_orbit_arbitrum_sepolia_contracts"


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


class MantleContracts(evmBasedContracts):
    __tablename__ = "mantle_contracts"


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


class MantleSepoliaContracts(evmBasedContracts):
    __tablename__ = "mantle_sepolia_contracts"


### Immutable zkEvm


class ImxZkevmBlockIndex(EvmBasedBlocks):
    __tablename__ = "imx_zkevm_blocks"


class ImxZkevmTransactionIndex(EvmBasedTransactions):
    __tablename__ = "imx_zkevm_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("imx_zkevm_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ImxZkevmLogIndex(EvmBasedLogs):
    __tablename__ = "imx_zkevm_logs"

    __table_args__ = (
        Index(
            "idx_imx_zkevm_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        Index(
            "idx_imx_zkevm_logs_block_hash_log_index",
            "block_hash",
            "log_index",
            unique=True,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_imx_zkevm_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_imx_zkevm_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("imx_zkevm_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ImxZkevmReorgs(EvmBasedReorgs):
    __tablename__ = "imx_zkevm_reorgs"


class ImxZkevmContracts(evmBasedContracts):
    __tablename__ = "imx_zkevm_contracts"


### Immutable zkEvm Sepolia


class ImxZkevmSepoliaBlockIndex(EvmBasedBlocks):
    __tablename__ = "imx_zkevm_sepolia_blocks"


class ImxZkevmSepoliaTransactionIndex(EvmBasedTransactions):
    __tablename__ = "imx_zkevm_sepolia_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("imx_zkevm_sepolia_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ImxZkevmSepoliaLogIndex(EvmBasedLogs):
    __tablename__ = "imx_zkevm_sepolia_logs"

    __table_args__ = (
        Index(
            "idx_imx_zkevm_sepolia_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        Index(
            "idx_imx_zkevm_sepolia_logs_block_hash_log_index",
            "block_hash",
            "log_index",
            unique=True,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_imx_zkevm_sepolia_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_imx_zkevm_sepolia_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("imx_zkevm_sepolia_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class ImxZkevmSepoliaReorgs(EvmBasedReorgs):
    __tablename__ = "imx_zkevm_sepolia_reorgs"


class ImxZkevmSepoliaContracts(evmBasedContracts):
    __tablename__ = "imx_zkevm_sepolia_contracts"


### Game7 Testnet
# Game7


class Game7BlockIndex(EvmBasedBlocks):
    __tablename__ = "game7_blocks"

    l1_block_number = Column(BigInteger, nullable=False)


class Game7Reorgs(EvmBasedReorgs):
    __tablename__ = "game7_reorgs"


class Game7Contracts(evmBasedContracts):
    __tablename__ = "game7_contracts"


# Game7 Testnet


class Game7TestnetBlockIndex(EvmBasedBlocks):
    __tablename__ = "game7_testnet_blocks"

    l1_block_number = Column(BigInteger, nullable=False)


class Game7TestnetTransactionIndex(EvmBasedTransactions):
    __tablename__ = "game7_testnet_transactions"

    block_number = Column(
        BigInteger,
        ForeignKey("game7_testnet_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class Game7TestnetLogIndex(EvmBasedLogs):
    __tablename__ = "game7_testnet_logs"

    __table_args__ = (
        Index(
            "idx_game7_testnet_logs_address_selector",
            "address",
            "selector",
            unique=False,
        ),
        UniqueConstraint(
            "transaction_hash",
            "log_index",
            name="uq_game7_testnet_log_index_transaction_hash_log_index",
        ),
        PrimaryKeyConstraint(
            "transaction_hash", "log_index", name="pk_game7_testnet_log_index"
        ),
    )
    transaction_hash = Column(
        VARCHAR(256),
        ForeignKey("game7_testnet_transactions.hash", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class Game7TestnetReorgs(EvmBasedReorgs):
    __tablename__ = "game7_testnet_reorgs"


class Game7TestnetContracts(evmBasedContracts):
    __tablename__ = "game7_testnet_contracts"


# B3
class B3BlockIndex(EvmBasedBlocks):
    __tablename__ = "b3_blocks"


class B3Reorgs(EvmBasedReorgs):
    __tablename__ = "b3_reorgs"


class B3Contracts(evmBasedContracts):
    __tablename__ = "b3_contracts"


class B3SepoliaBlockIndex(EvmBasedBlocks):
    __tablename__ = "b3_sepolia_blocks"


class B3SepoliaReorgs(EvmBasedReorgs):
    __tablename__ = "b3_sepolia_reorgs"


class B3SepoliaContracts(evmBasedContracts):
    __tablename__ = "b3_sepolia_contracts"


class RoninBlockIndex(EvmBasedBlocks):
    __tablename__ = "ronin_blocks"


class RoninReorgs(EvmBasedReorgs):
    __tablename__ = "ronin_reorgs"


class RoninContracts(evmBasedContracts):
    __tablename__ = "ronin_contracts"


class RoninSaigonBlockIndex(EvmBasedBlocks):
    __tablename__ = "ronin_saigon_blocks"


class RoninSaigonReorgs(EvmBasedReorgs):
    __tablename__ = "ronin_saigon_reorgs"


class RoninSaigonContracts(evmBasedContracts):
    __tablename__ = "ronin_saigon_contracts"


### ABI Jobs


class AbiJobs(Base):
    __tablename__ = "abi_jobs"

    __table_args__ = (
        UniqueConstraint(
            "chain",
            "address",
            "abi_selector",
            "customer_id",
            name="uq_abi_jobs",
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
    deployment_block_number = Column(BigInteger, nullable=True, index=False)
    abi = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class AbiSubscriptions(Base):
    __tablename__ = "abi_subscriptions"

    __table_args__ = (PrimaryKeyConstraint("abi_job_id", "subscription_id"),)

    abi_job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("abi_jobs.id"),
        nullable=False,
        index=True,
    )
    subscription_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class BytecodeStorage(Base):

    __tablename__ = "bytecode_storage"

    __table_args__ = (UniqueConstraint("hash", name="uq_bytecode_storage_hash"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash = Column(VARCHAR(32), nullable=False, index=True)
    bytecode = Column(Text, nullable=False)
    title = Column(VARCHAR(256), nullable=True)
    description = Column(Text, nullable=True)
    abi = Column(JSONB, nullable=True)
    code = Column(Text, nullable=True)  # source code
    data = Column(JSONB, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )
