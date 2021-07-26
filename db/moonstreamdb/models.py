from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    ForeignKey,
    MetaData,
    Text,
    VARCHAR,
)
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

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
    type = DateTime


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kwargs):
    return "TIMEZONE('utc', statement_timestamp())"


class EthereumBlock(Base):  # type: ignore
    __tablename__ = "ethereum_blocks"

    block_number = Column(
        BigInteger,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    difficulty = Column(BigInteger)
    extra_data = Column(VARCHAR(128))
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    hash = Column(VARCHAR(256))
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
        VARCHAR(256),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    block_number = Column(
        BigInteger,
        ForeignKey("ethereum_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
    )
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Text)
    gas_price = Column(Text)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    value = Column(Text)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )


class EthereumPendingTransaction(Base):  # type: ignore
    __tablename__ = "ethereum_pending_transactions"

    hash = Column(
        VARCHAR(256),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    block_number = Column(
        BigInteger,
        ForeignKey("ethereum_blocks.block_number", ondelete="CASCADE"),
        nullable=False,
    )
    from_address = Column(VARCHAR(256), index=True)
    to_address = Column(VARCHAR(256), index=True)
    gas = Column(Text)
    gas_price = Column(Text)
    input = Column(Text)
    nonce = Column(VARCHAR(256))
    transaction_index = Column(BigInteger)
    value = Column(Text)

    indexed_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
