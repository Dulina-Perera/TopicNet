# %%
# Import the required classes, functions, and modules.
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import Index, PrimaryKeyConstraint

from ..core_.database_ import Base

# %%
class Document(Base):
  __tablename__ = "_document"

  id: Mapped[int] = mapped_column(autoincrement="auto")
  path: Mapped[str] = mapped_column(nullable=False, unique=True)

  __table_args__ = (
		PrimaryKeyConstraint("id"),
		Index("ix_document_path", "path")
	)

  @classmethod
  async def create(cls, session: AsyncSession, path: str) -> "Document":
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
    document: Document = cls(path=path)

    # Add the document record to the session and commit the transaction.
    try:
      session.add(document)
      await session.commit()
      await session.refresh(document)

      return document
    except Exception as e:
      await session.rollback()
      raise e
