from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

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
    EthereumLabel,
    SepoliaLabel,
    PolygonLabel,
    MumbaiLabel,
    AmoyLabel,
    XDaiLabel,
    ZkSyncEraLabel,
    ZkSyncEraSepoliaLabel,
    BaseLabel,
    ArbitrumNovaLabel,
    ArbitrumOneLabel,
    ArbitrumSepoliaLabel,
    Game7OrbitArbitrumSepoliaLabel,
    XaiLabel,
    XaiSepoliaLabel,
    AvalancheLabel,
    AvalancheFujiLabel,
    BlastLabel,
    BlastSepoliaLabel,
    ProofOfPlayApexLabel,
    StarknetLabel,
    StarknetSepoliaLabel,
    MantleLabel,
    MantleSepoliaLabel,
)


def include_symbol(tablename, schema):
    return tablename in {
        EthereumLabel.__tablename__,
        SepoliaLabel.__tablename__,
        PolygonLabel.__tablename__,
        MumbaiLabel.__tablename__,
        AmoyLabel.__tablename__,
        XDaiLabel.__tablename__,
        ZkSyncEraLabel.__tablename__,
        ZkSyncEraSepoliaLabel.__tablename__,
        BaseLabel.__tablename__,
        ArbitrumNovaLabel.__tablename__,
        ArbitrumOneLabel.__tablename__,
        ArbitrumSepoliaLabel.__tablename__,
        Game7OrbitArbitrumSepoliaLabel.__tablename__,
        XaiLabel.__tablename__,
        XaiSepoliaLabel.__tablename__,
        AvalancheLabel.__tablename__,
        AvalancheFujiLabel.__tablename__,
        BlastLabel.__tablename__,
        BlastSepoliaLabel.__tablename__,
        ProofOfPlayApexLabel.__tablename__,
        StarknetLabel.__tablename__,
        StarknetSepoliaLabel.__tablename__,
        MantleLabel.__tablename__,
        MantleSepoliaLabel.__tablename__,
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
