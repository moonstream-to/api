from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from moonstreamdb.models import Base as MoonstreamBase

target_metadata = MoonstreamBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
from moonstreamdb.models import (
    ESDEventSignature,
    ESDFunctionSignature,
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    MumbaiBlock,
    MumbaiLabel,
    MumbaiTransaction,
    OpenSeaCrawlingState,
    PolygonBlock,
    PolygonLabel,
    PolygonTransaction,
    WyrmBlock,
    WyrmLabel,
    WyrmTransaction,
    XDaiBlock,
    XDaiLabel,
    XDaiTransaction,
    ZkSyncEraTestnetBlock,
    ZkSyncEraTestnetLabel,
    ZkSyncEraTestnetTransaction,
)


def include_symbol(tablename, schema):
    return tablename in {
        EthereumBlock.__tablename__,
        EthereumTransaction.__tablename__,
        EthereumLabel.__tablename__,
        PolygonBlock.__tablename__,
        PolygonTransaction.__tablename__,
        PolygonLabel.__tablename__,
        MumbaiBlock.__tablename__,
        MumbaiTransaction.__tablename__,
        MumbaiLabel.__tablename__,
        ESDFunctionSignature.__tablename__,
        ESDEventSignature.__tablename__,
        OpenSeaCrawlingState.__tablename__,
        WyrmBlock.__tablename__,
        WyrmLabel.__tablename__,
        WyrmTransaction.__tablename__,
        XDaiBlock.__tablename__,
        XDaiLabel.__tablename__,
        XDaiTransaction.__tablename__,
        ZkSyncEraTestnetBlock.__tablename__,
        ZkSyncEraTestnetLabel.__tablename__,
        ZkSyncEraTestnetTransaction.__tablename__,
    }


def run_migrations_offline():
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
        version_table="alembic_exploration_version",
        include_symbol=include_symbol,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_exploration_version",
            include_symbol=include_symbol,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
