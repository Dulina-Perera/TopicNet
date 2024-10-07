# %%
# Import the required modules.
from fastapi import Depends
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session, sessionmaker
from typing import Annotated, Any, Dict, Generator, Union

from .config import load_db_config

# %%
# Database configuration
DB_CONFIG: Dict[str, Union[int, str]] = load_db_config()

# Database URL
DB_URL: str = f"{DB_CONFIG['dialect']}+{DB_CONFIG['driver']}://" \
							f"{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
							f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine: Engine = create_engine(url=DB_URL, echo=True)  # Database engine
SessionLocal: scoped_session[Session] = scoped_session(
  sessionmaker(autocommit=False, autoflush=False, bind=engine)
)  # A scoped session that is thread-safe

# Base class for all the ORM models
Base: Any = declarative_base()

# %%
def init_db() -> None:
  """
  Initialize the database.

	This function creates the database tables if they do not exist.

	Parameters:
		None

	Returns:
		None
  """
  from ..models import Document, Node, Sentence

  # Drop all tables in the database.
  Base.metadata.drop_all(bind=engine)

  # Create all tables in the database.
  Base.metadata.create_all(bind=engine)


def get_db_session() -> Generator[Any, Any, Any]:
  """
  Get a new database session.

	This function returns a new database session that can be used to interact with the database.

	Parameters:
		None

	Returns:
		scoped_session: The database session
  """
  db_session: scoped_session[Session] = SessionLocal()

  try:
    yield db_session
  except SQLAlchemyError:
    raise
  finally:
    db_session.close()

# %%
# Database session dependency
db_session_dep = Annotated[scoped_session[Session], Depends(get_db_session)]

# %%
if __name__ == "__main__":
	init_db()
