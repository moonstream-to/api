from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from moonstreamdbv3.models import Base as MoonstreamBase

target_metadata = MoonstreamBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
from moonstreamdbv3.models import (
    MOONSTREAM_DB_V3_SCHEMA_NAME,
    AmoyLabel,
    AmoyTransaction,
    ArbitrumNovaLabel,
    ArbitrumNovaTransaction,
    ArbitrumOneLabel,
    ArbitrumOneTransaction,
    ArbitrumSepoliaLabel,
    ArbitrumSepoliaTransaction,
    AvalancheFujiLabel,
    AvalancheFujiTransaction,
    AvalancheLabel,
    AvalancheTransaction,
    B3Label,
    B3Transaction,
    B3SepoliaLabel,
    B3SepoliaTransaction,
    BaseLabel,
    BaseTransaction,
    BlastLabel,
    BlastTransaction,
    BlastSepoliaLabel,
    BlastSepoliaTransaction,
    EthereumLabel,
    EthereumTransaction,
    Game7Label,
    Game7Transaction,
    Game7OrbitArbitrumSepoliaLabel,
    Game7OrbitArbitrumSepoliaTransaction,
    Game7TestnetLabel,
    Game7TestnetTransaction,
    ImxZkevmLabel,
    ImxZkevmTransaction,
    ImxZkevmSepoliaLabel,
    ImxZkevmSepoliaTransaction,
    MantleLabel,
    MantleTransaction,
    MantleSepoliaLabel,
    MantleSepoliaTransaction,
    MumbaiLabel,
    MumbaiTransaction,
    PolygonLabel,
    PolygonTransaction,
    ProofOfPlayApexLabel,
    ProofOfPlayApexTransaction,
    RoninLabel,
    RoninSaigonLabel,
    SepoliaLabel,
    SepoliaTransaction,
    StarknetLabel,
    StarknetSepoliaLabel,
    XaiLabel,
    XaiTransaction,
    XaiSepoliaLabel,
    XaiSepoliaTransaction,
    XDaiLabel,
    XDaiTransaction,
    ZkSyncEraLabel,
    ZkSyncEraTransaction,
    ZkSyncEraSepoliaLabel,
    ZkSyncEraSepoliaTransaction,
)


def include_symbol(tablename, schema):
    return tablename in {
        EthereumLabel.__tablename__,
        EthereumTransaction.__tablename__,
        SepoliaLabel.__tablename__,
        SepoliaTransaction.__tablename__,
        PolygonLabel.__tablename__,
        PolygonTransaction.__tablename__,
        MumbaiLabel.__tablename__,
        MumbaiTransaction.__tablename__,
        AmoyLabel.__tablename__,
        AmoyTransaction.__tablename__,
        XDaiLabel.__tablename__,
        XDaiTransaction.__tablename__,
        ZkSyncEraLabel.__tablename__,
        ZkSyncEraTransaction.__tablename__,
        ZkSyncEraSepoliaLabel.__tablename__,
        ZkSyncEraSepoliaTransaction.__tablename__,
        BaseLabel.__tablename__,
        BaseTransaction.__tablename__,
        ArbitrumNovaLabel.__tablename__,
        ArbitrumNovaTransaction.__tablename__,
        ArbitrumOneLabel.__tablename__,
        ArbitrumOneTransaction.__tablename__,
        ArbitrumSepoliaLabel.__tablename__,
        ArbitrumSepoliaTransaction.__tablename__,
        Game7Label.__tablename__,
        Game7Transaction.__tablename__,
        Game7OrbitArbitrumSepoliaLabel.__tablename__,
        Game7OrbitArbitrumSepoliaTransaction.__tablename__,
        Game7TestnetLabel.__tablename__,
        Game7TestnetTransaction.__tablename__,
        XaiLabel.__tablename__,
        XaiTransaction.__tablename__,
        XaiSepoliaLabel.__tablename__,
        XaiSepoliaTransaction.__tablename__,
        AvalancheLabel.__tablename__,
        AvalancheTransaction.__tablename__,
        AvalancheFujiLabel.__tablename__,
        AvalancheFujiTransaction.__tablename__,
        BlastLabel.__tablename__,
        BlastTransaction.__tablename__,
        BlastSepoliaLabel.__tablename__,
        BlastSepoliaTransaction.__tablename__,
        ProofOfPlayApexLabel.__tablename__,
        ProofOfPlayApexTransaction.__tablename__,
        StarknetLabel.__tablename__,
        StarknetSepoliaLabel.__tablename__,
        MantleLabel.__tablename__,
        MantleTransaction.__tablename__,
        MantleSepoliaLabel.__tablename__,
        MantleSepoliaTransaction.__tablename__,
        ImxZkevmLabel.__tablename__,
        ImxZkevmTransaction.__tablename__,
        ImxZkevmSepoliaLabel.__tablename__,
        ImxZkevmSepoliaTransaction.__tablename__,
        B3Label.__tablename__,
        B3Transaction.__tablename__,
        B3SepoliaLabel.__tablename__,
        B3SepoliaTransaction.__tablename__,
        RoninLabel.__tablename__,
        RoninSaigonLabel.__tablename__,
    }


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table="alembic_version",
        version_table_schema=MOONSTREAM_DB_V3_SCHEMA_NAME,
        include_schemas=True,
        include_symbol=include_symbol,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version",
            version_table_schema=MOONSTREAM_DB_V3_SCHEMA_NAME,
            include_schemas=True,
            include_symbol=include_symbol,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
