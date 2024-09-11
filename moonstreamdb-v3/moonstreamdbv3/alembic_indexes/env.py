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
from moonstreamdbv3.models_indexes import Base as MoonstreamBase

target_metadata = MoonstreamBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

from moonstreamdbv3.models_indexes import (
    AbiJobs,
    AbiSubscriptions,
    ArbitrumOneBlockIndex,
    ArbitrumOneLogIndex,
    ArbitrumOneReorgs,
    ArbitrumOneTransactionIndex,
    ArbitrumSepoliaBlockIndex,
    ArbitrumSepoliaLogIndex,
    ArbitrumSepoliaReorgs,
    ArbitrumSepoliaTransactionIndex,
    B3BlockIndex,
    B3Reorgs,
    B3SepoliaBlockIndex,
    B3SepoliaReorgs,
    EthereumBlockIndex,
    EthereumLogIndex,
    EthereumReorgs,
    EthereumTransactionIndex,
    Game7OrbitArbitrumSepoliaBlockIndex,
    Game7OrbitArbitrumSepoliaLogIndex,
    Game7OrbitArbitrumSepoliaReorgs,
    Game7OrbitArbitrumSepoliaTransactionIndex,
    Game7TestnetBlockIndex,
    Game7TestnetLogIndex,
    Game7TestnetReorgs,
    Game7TestnetTransactionIndex,
    ImxZkevmBlockIndex,
    ImxZkevmLogIndex,
    ImxZkevmReorgs,
    ImxZkevmSepoliaBlockIndex,
    ImxZkevmSepoliaLogIndex,
    ImxZkevmSepoliaReorgs,
    ImxZkevmSepoliaTransactionIndex,
    ImxZkevmTransactionIndex,
    MantleBlockIndex,
    MantleLogIndex,
    MantleReorgs,
    MantleSepoliaBlockIndex,
    MantleSepoliaLogIndex,
    MantleSepoliaReorgs,
    MantleSepoliaTransactionIndex,
    MantleTransactionIndex,
    PolygonBlockIndex,
    PolygonLogIndex,
    PolygonReorgs,
    PolygonTransactionIndex,
    XaiBlockIndex,
    XaiLogIndex,
    XaiReorgs,
    XaiSepoliaBlockIndex,
    XaiSepoliaLogIndex,
    XaiSepoliaReorgs,
    XaiSepoliaTransactionIndex,
    XaiTransactionIndex,
)


def include_symbol(tablename, schema):
    return tablename in {
        EthereumBlockIndex.__tablename__,
        EthereumTransactionIndex.__tablename__,
        EthereumLogIndex.__tablename__,
        EthereumReorgs.__tablename__,
        PolygonBlockIndex.__tablename__,
        PolygonTransactionIndex.__tablename__,
        PolygonLogIndex.__tablename__,
        PolygonReorgs.__tablename__,
        XaiBlockIndex.__tablename__,
        XaiTransactionIndex.__tablename__,
        XaiLogIndex.__tablename__,
        XaiReorgs.__tablename__,
        XaiSepoliaBlockIndex.__tablename__,
        XaiSepoliaTransactionIndex.__tablename__,
        XaiSepoliaLogIndex.__tablename__,
        XaiSepoliaReorgs.__tablename__,
        ArbitrumOneBlockIndex.__tablename__,
        ArbitrumOneTransactionIndex.__tablename__,
        ArbitrumOneLogIndex.__tablename__,
        ArbitrumOneReorgs.__tablename__,
        ArbitrumSepoliaBlockIndex.__tablename__,
        ArbitrumSepoliaTransactionIndex.__tablename__,
        ArbitrumSepoliaLogIndex.__tablename__,
        ArbitrumSepoliaReorgs.__tablename__,
        Game7OrbitArbitrumSepoliaBlockIndex.__tablename__,
        Game7OrbitArbitrumSepoliaTransactionIndex.__tablename__,
        Game7OrbitArbitrumSepoliaLogIndex.__tablename__,
        Game7OrbitArbitrumSepoliaReorgs.__tablename__,
        Game7TestnetBlockIndex.__tablename__,
        Game7TestnetTransactionIndex.__tablename__,
        Game7TestnetLogIndex.__tablename__,
        Game7TestnetReorgs.__tablename__,
        MantleBlockIndex.__tablename__,
        MantleTransactionIndex.__tablename__,
        MantleLogIndex.__tablename__,
        MantleReorgs.__tablename__,
        MantleSepoliaBlockIndex.__tablename__,
        MantleSepoliaTransactionIndex.__tablename__,
        MantleSepoliaLogIndex.__tablename__,
        MantleSepoliaReorgs.__tablename__,
        AbiJobs.__tablename__,
        AbiSubscriptions.__tablename__,
        ImxZkevmBlockIndex.__tablename__,
        ImxZkevmTransactionIndex.__tablename__,
        ImxZkevmLogIndex.__tablename__,
        ImxZkevmReorgs.__tablename__,
        ImxZkevmSepoliaBlockIndex.__tablename__,
        ImxZkevmSepoliaTransactionIndex.__tablename__,
        ImxZkevmSepoliaLogIndex.__tablename__,
        ImxZkevmSepoliaReorgs.__tablename__,
        B3BlockIndex.__tablename__,
        B3Reorgs.__tablename__,
        B3SepoliaBlockIndex.__tablename__,
        B3SepoliaReorgs.__tablename__,
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
            include_schemas=True,
            include_symbol=include_symbol,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
