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
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base, declared_attr
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

    @declared_attr
    def __table_args__(cls):
        return (
            Index(
                f"ix_{cls.__tablename__}_addr_block_num",
                "address", "block_number", unique=False
            ),
            Index(
                f"ix_{cls.__tablename__}_addr_block_ts",
                "address", "block_timestamp", unique=False
            ),
            Index(
                f"ix_{cls.__tablename__}_label_addr_name",
                "label", "address", "label_name", unique=False
            ),
            Index(
                f"uk_{cls.__tablename__}_tx_hash_tx_call",
                "transaction_hash", unique=True,
                postgresql_where=text("label='seer' and label_type='tx_call'")
            ),
            Index(
                f"uk_{cls.__tablename__}_tx_hash_log_idx_evt",
                "transaction_hash", "log_index", unique=True,
                postgresql_where=text("label='seer' and label_type='event'")
            ),
            Index(
                f"uk_{cls.__tablename__}_tx_hash_tx_call_raw",
                "transaction_hash", unique=True,
                postgresql_where=text("label='seer-raw' and label_type='tx_call'")
            ),
            Index(
                f"uk_{cls.__tablename__}_tx_hash_log_idx_evt_raw",
                "transaction_hash", "log_index", unique=True,
                postgresql_where=text("label='seer-raw' and label_type='event'")
            )
        )
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
        nullable=True,
        index=True,
    )
    log_index = Column(Integer, nullable=True)

    block_number = Column(
        BigInteger,
        nullable=False,
        index=True,
    )
    block_hash = Column(VARCHAR(256), nullable=True)
    block_timestamp = Column(BigInteger, nullable=True)

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
    block_number = Column(
            BigInteger,
            nullable=False,
            index=True,
        )
    block_timestamp = Column(BigInteger, nullable=False, index=True)
    block_hash = Column(VARCHAR(256), nullable=False, index=True)
    from_address = Column(LargeBinary, index=True)
    to_address = Column(LargeBinary, index=True)
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


## Labels

class EthereumLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "ethereum_labels"

class SepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "sepolia_labels"

class PolygonLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "polygon_labels"

class MumbaiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "mumbai_labels"

class AmoyLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "amoy_labels"

class XDaiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "xdai_labels"

class ZkSyncEraLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "zksync_era_labels"

class ZkSyncEraSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "zksync_era_sepolia_labels"

class BaseLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "base_labels"

class ArbitrumNovaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "arbitrum_nova_labels"

class ArbitrumOneLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "arbitrum_one_labels"

class ArbitrumSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "arbitrum_sepolia_labels"

class Game7OrbitArbitrumSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "game7_orbit_arbitrum_sepolia_labels"

class XaiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "xai_labels"

class XaiSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "xai_sepolia_labels"

class AvalancheLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "avalanche_labels"

class AvalancheFujiLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "avalanche_fuji_labels"

class BlastLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "blast_labels"

class BlastSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "blast_sepolia_labels"

class ProofOfPlayApexLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "proofofplay_apex_labels"

class StarknetLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "starknet_labels"

class StarknetSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "starknet_sepolia_labels"

class MantleLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "mantle_labels"

class MantleSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "mantle_sepolia_labels"

class ImxZkevmLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "imx_zkevm_labels"

class ImxZkevmSepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "imx_zkevm_sepolia_labels"

class Game7Label(EvmBasedLabel):  # type: ignore
    __tablename__ = "game7_labels"

class Game7TestnetLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "game7_testnet_labels"

class B3Label(EvmBasedLabel):  # type: ignore
    __tablename__ = "b3_labels"

class B3SepoliaLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "b3_sepolia_labels"

class RoninLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "ronin_labels"

class RoninSaigonLabel(EvmBasedLabel):  # type: ignore
    __tablename__ = "ronin_saigon_labels"





## Transactions

class EthereumTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "ethereum_transactions"


class SepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "sepolia_transactions"


class PolygonTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "polygon_transactions"


class MumbaiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "mumbai_transactions"


class AmoyTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "amoy_transactions"


class XDaiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "xdai_transactions"


class ZkSyncEraTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "zksync_era_transactions"


class ZkSyncEraSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "zksync_era_sepolia_transactions"


class BaseTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "base_transactions"


class ArbitrumNovaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "arbitrum_nova_transactions"

    l1_block_number = Column(BigInteger, nullable=True)

class ArbitrumOneTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "arbitrum_one_transactions"

    l1_block_number = Column(BigInteger, nullable=True)

class ArbitrumSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "arbitrum_sepolia_transactions"

    l1_block_number = Column(BigInteger, nullable=True)

class Game7OrbitArbitrumSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "game7_orbit_arbitrum_sepolia_transactions"

    l1_block_number = Column(BigInteger, nullable=True)

class XaiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "xai_transactions"

    l1_block_number = Column(BigInteger, nullable=True)

class XaiSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "xai_sepolia_transactions"

    l1_block_number = Column(BigInteger, nullable=True)

class AvalancheTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "avalanche_transactions"

class AvalancheFujiTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "avalanche_fuji_transactions"

class BlastTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "blast_transactions"

class BlastSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "blast_sepolia_transactions"


class ProofOfPlayApexTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "proofofplay_apex_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


class MantleTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "mantle_transactions"


class MantleSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "mantle_sepolia_transactions"


class ImxZkevmTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "imx_zkevm_transactions"


class ImxZkevmSepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "imx_zkevm_sepolia_transactions"


class Game7Transaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "game7_transactions"

    l1_block_number = Column(BigInteger, nullable=True)



class Game7TestnetTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "game7_testnet_transactions"

    l1_block_number = Column(BigInteger, nullable=True)


class B3Transaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "b3_transactions"



class B3SepoliaTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "b3_sepolia_transactions"


class RoninTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "ronin_transactions"


class RoninSaigonTransaction(EvmBasedTransaction):  # type: ignore
    __tablename__ = "ronin_saigon_transactions"
