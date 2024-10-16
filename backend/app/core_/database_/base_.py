# %%
# Import the required modules.
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
  AsyncEngine,
  AsyncSession,
  async_scoped_session,
  async_sessionmaker,
  create_async_engine
)
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session
from typing import Annotated, Any, AsyncGenerator, Dict, Union

from ..config_ import load_db_config
from ...exceptions_ import DatabaseInitializationError

# %%
# Database configuration
DB_CONFIG: Dict[str, Union[int, str]] = load_db_config()

# Database URL
DB_URL: str = f"{DB_CONFIG['dialect']}+{DB_CONFIG['driver']}://" \
							f"{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
							f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine: AsyncEngine = create_async_engine(DB_URL, echo=True)  # The async database engine
AsyncSessionLocal: async_scoped_session[AsyncSession] = async_scoped_session(
  async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
  ),
  scopefunc=lambda: None
)  # The async database session

# Base class for all the ORM models
class Base(DeclarativeBase):
  pass

# %%
async def init_db() -> None:
  """
  Initialize the database.

	This function creates the database tables if they do not exist.
  """
  # Import the models.
  from ...models_ import Document, Node, Sentence

	# Use the async engine to create tables in an async context.
  async with engine.begin() as conn:
    try:
      # Create all tables if they do not exist.
      await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as e:
      raise DatabaseInitializationError(f"Database initialization error: {str(e)}")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
  """
  Get a new database session.

	This function returns a new database session that can be used to interact with the database.

	:returns: A new database session
	:rtype: Generator[AsyncSession, None, None]
  """
  # Create a new database session.
  db_session: async_scoped_session[AsyncSession] = AsyncSessionLocal()

	# Yield the database session and close it after use.
  try:
    yield db_session
  finally:
    await db_session.close()

# %%
# Asynchronous database session dependency
async_db_session_dep = Annotated[async_scoped_session[AsyncSession], Depends(get_db_session)]
