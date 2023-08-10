import uuid

from sqlalchemy import (
    DECIMAL,
    VARCHAR,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import and_, expression

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


class DropperContract(Base):  # type: ignore
    __tablename__ = "dropper_contracts"
    __table_args__ = (UniqueConstraint("blockchain", "address"),)

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    blockchain = Column(VARCHAR(128), nullable=False)
    address = Column(VARCHAR(256), index=True)
    title = Column(VARCHAR(128), nullable=True)
    description = Column(String, nullable=True)
    image_uri = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )


class DropperClaim(Base):  # type: ignore
    __tablename__ = "dropper_claims"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    dropper_contract_id = Column(
        UUID(as_uuid=True),
        ForeignKey("dropper_contracts.id", ondelete="CASCADE"),
        nullable=False,
    )
    claim_id = Column(BigInteger, nullable=True)
    title = Column(VARCHAR(128), nullable=True)
    description = Column(String, nullable=True)
    terminus_address = Column(VARCHAR(256), nullable=True, index=True)
    terminus_pool_id = Column(BigInteger, nullable=True, index=True)
    claim_block_deadline = Column(BigInteger, nullable=True)
    active = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "uq_dropper_claims_dropper_contract_id_claim_id",
            "dropper_contract_id",
            "claim_id",
            unique=True,
            postgresql_where=and_(claim_id.isnot(None), active.is_(True)),
        ),
    )


class DropperClaimant(Base):  # type: ignore
    __tablename__ = "dropper_claimants"
    __table_args__ = (UniqueConstraint("dropper_claim_id", "address"),)

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    dropper_claim_id = Column(
        UUID(as_uuid=True),
        ForeignKey("dropper_claims.id", ondelete="CASCADE"),
        nullable=False,
    )
    address = Column(VARCHAR(256), nullable=False, index=True)
    amount = Column(BigInteger, nullable=False)
    raw_amount = Column(String, nullable=True)
    added_by = Column(VARCHAR(256), nullable=False, index=True)
    signature = Column(String, nullable=True, index=True)

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )


class CallRequestType(Base):  # type: ignore
    """
    CallRequestType contains versions of call requests like:
    raw or dropper-v0.2.0.
    """

    __tablename__ = "call_request_types"

    name = Column(
        VARCHAR(128),
        primary_key=True,
        unique=True,
    )
    description = Column(String, nullable=True)


class MetatxRequester(Base):  # type: ignore
    """
    MetatxRequester represents id of user from bugout authorization.
    """

    __tablename__ = "metatx_requesters"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
    )

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )

    registered_contracts = relationship(
        "RegisteredContract",
        back_populates="metatx_requester",
        cascade="all, delete, delete-orphan",
    )
    call_requests = relationship(
        "CallRequest",
        back_populates="metatx_requester",
        cascade="all, delete, delete-orphan",
    )


class Blockchain(Base):  # type: ignore
    __tablename__ = "blockchains"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    name = Column(VARCHAR(128), nullable=False, index=True, unique=True)
    chain_id = Column(Integer, nullable=False, index=True, unique=False)
    testnet = Column(Boolean, default=False, nullable=False)

    registered_contracts = relationship(
        "RegisteredContract",
        back_populates="blockchain",
        cascade="all, delete, delete-orphan",
    )


class RegisteredContract(Base):  # type: ignore
    __tablename__ = "registered_contracts"
    __table_args__ = (
        UniqueConstraint(
            "blockchain_id",
            "metatx_requester_id",
            "address",
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    metatx_requester_id = Column(
        UUID(as_uuid=True),
        ForeignKey("metatx_requesters.id", ondelete="CASCADE"),
        nullable=False,
    )
    blockchain_id = Column(
        UUID(as_uuid=True),
        ForeignKey("blockchains.id", ondelete="CASCADE"),
        nullable=False,
    )

    address = Column(VARCHAR(256), nullable=False, index=True)
    title = Column(VARCHAR(128), nullable=False)
    description = Column(String, nullable=True)
    image_uri = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )

    call_requests = relationship(
        "CallRequest",
        back_populates="registered_contract",
        cascade="all, delete, delete-orphan",
    )

    metatx_requester = relationship(
        "MetatxRequester", back_populates="registered_contracts"
    )
    blockchain = relationship("Blockchain", back_populates="registered_contracts")


class CallRequest(Base):
    __tablename__ = "call_requests"
    __table_args__ = (
        UniqueConstraint(
            "registered_contract_id",
            "request_id",
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    registered_contract_id = Column(
        UUID(as_uuid=True),
        ForeignKey("registered_contracts.id", ondelete="CASCADE"),
        nullable=False,
    )
    call_request_type_name = Column(
        VARCHAR(128),
        ForeignKey("call_request_types.name", ondelete="CASCADE"),
        nullable=False,
    )
    metatx_requester_id = Column(
        UUID(as_uuid=True),
        ForeignKey("metatx_requesters.id", ondelete="CASCADE"),
        nullable=False,
    )

    caller = Column(VARCHAR(256), nullable=False, index=True)
    method = Column(String, nullable=False, index=True)
    request_id = Column(DECIMAL, nullable=False, index=True)
    parameters = Column(JSONB, nullable=False)

    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)

    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )

    registered_contract = relationship(
        "RegisteredContract", back_populates="call_requests"
    )
    metatx_requester = relationship("MetatxRequester", back_populates="call_requests")


class Leaderboard(Base):  # type: ignore
    __tablename__ = "leaderboards"
    # __table_args__ = (UniqueConstraint("dropper_contract_id", "address"),)

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(VARCHAR(128), nullable=False)
    description = Column(String, nullable=True)
    resource_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )


class LeaderboardScores(Base):  # type: ignore
    __tablename__ = "leaderboard_scores"
    __table_args__ = (UniqueConstraint("leaderboard_id", "address"),)

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    leaderboard_id = Column(
        UUID(as_uuid=True),
        ForeignKey("leaderboards.id", ondelete="CASCADE"),
        nullable=False,
    )
    address = Column(VARCHAR(256), nullable=False, index=True)
    score = Column(BigInteger, nullable=False)
    points_data = Column(JSONB, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=utcnow(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
        nullable=False,
    )
