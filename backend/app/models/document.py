# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

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

  @classmethod
  def create(cls, session: Session, path: str) -> "Document":
    """
		Create a new document record in the database.

		:param session: The database session
		:type session: Session

		:param path: The path where the document is actually stored
		:type path: str

		:return: The newly created document record
		:rtype: Document
    """
		# Create a new document record.
    document: Document = cls(path)

    # Add the document record to the session and commit the transaction.
    try:
      session.add(document)
      session.commit()

      return document
    except Exception as e:
      session.rollback()
      raise e
