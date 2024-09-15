# backend/models.py

# %%
# Import the necessary modules.
import warnings; warnings.filterwarnings('ignore')

import yaml

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String
from typing import Any, Dict

# %%
Base: Any = declarative_base() # Create a base class for the ORM.

# Load the database configuration from the YAML file.
with open('config/db_config.yaml', 'r') as f:
  db_config: Dict[str, Any] = yaml.safe_load(f.read())

# Create the database connection url.
db_url: str = f"{db_config['dialect']}+{db_config['driver']}://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Create the database engine and session.
engine: Engine = create_engine(url=db_url, echo=True)
SessionLocal: Any = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# %%
# Define the database models.
class Document(Base):
	__tablename__ = 'document'

	id = Column(
  	type_=Integer,
		autoincrement='ignore_fk',
   	primary_key=True
  )
	path = Column(
   	type_=String,
    index=True,
    unique=True,
    nullable=False
  )

class Node(Base):
	__tablename__ = 'node'

	id = Column(
	 	type_=Integer,
		autoincrement='ignore_fk',
		primary_key=True
	)
	parent_id = Column(
		ForeignKey('node.id'),
		type_=Integer
	)
	document_id = Column(
		ForeignKey('document.id'),
		type_=Integer,
		nullable=False
	)
	topic = Column(
	 	type_=String,
		index=True
	)
	content = Column(type_=String)

class Sentence(Base):
	__tablename__ = 'sentence'

	id = Column(
	 	type_=Integer,
		autoincrement='auto',
		primary_key=True
	)
	document_id = Column(
		ForeignKey('document.id'),
		type_=Integer,
		nullable=False
	)
	node_id = Column(
		ForeignKey('node.id'),
		type_=Integer
	)
	content = Column(
	 	type_=String,
		nullable=False
	)
	embeddings = Column(type_=ARRAY(Float))

# %%
if __name__ == '__main__':
  # Drop all tables in the database.
  Base.metadata.drop_all(bind=engine)

  # Create all tables in the database.
  Base.metadata.create_all(bind=engine)
