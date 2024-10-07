# %%
# Import the required modules.
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String

from ..core.database import Base

# %%
class Document(Base):
	__tablename__ = "document"

	id = Column(
  	type_=Integer,
		autoincrement="ignore_fk",
   	primary_key=True
  )
	path = Column(
   	type_=String,
    index=True,
    unique=True,
    nullable=False
  )

class Node(Base):
	__tablename__ = "node"

	id = Column(
	 	type_=Integer,
		autoincrement="ignore_fk",
		primary_key=True
	)
	parent_id = Column(
		ForeignKey("node.id"),
		type_=Integer
	)
	document_id = Column(
		ForeignKey("document.id"),
		type_=Integer,
		nullable=False
	)
	topic = Column(
	 	type_=String,
		index=True
	)
	content = Column(type_=String)

class Sentence(Base):
	__tablename__ = "sentence"

	id = Column(
	 	type_=Integer,
		autoincrement="auto",
		primary_key=True
	)
	document_id = Column(
		ForeignKey("document.id"),
		type_=Integer,
		nullable=False
	)
	node_id = Column(
		ForeignKey("node.id"),
		type_=Integer
	)
	content = Column(
	 	type_=String,
		nullable=False
	)
	embeddings = Column(type_=ARRAY(Float))
