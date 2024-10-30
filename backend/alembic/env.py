# %%
# Import the required libraries, modules, classes, and functions.
import asyncio

from alembic import context
from alembic.config import Config
from logging.config import fileConfig
from sqlalchemy.pool import NullPool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from typing import Any, Dict, Union

from app.core_ import load_db_config
from app.core_.database_ import Base
from app.models_ import Document, Node, Sentence, Session, User

# %%
# The Alembic config object, which provides access to the values within the .ini file in use.
config: Config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
  fileConfig(config.config_file_name)

# Metadata object of the data model
target_metadata: Any = Base.metadata

# Set the URL of the database.
## Database configuration
DB_CONFIG: Dict[str, Union[int, str]] = load_db_config()

## Database URL
DB_URL: str = f"{DB_CONFIG['dialect']}+{DB_CONFIG['driver']}://" \
							f"{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
							f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
config.set_main_option("sqlalchemy.url", DB_URL)

# %%
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
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
