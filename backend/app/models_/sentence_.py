# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKeyConstraint, Index, PrimaryKeyConstraint

from ..core_.database_ import Base

# %%
class Sentence(Base):
  __tablename__ = "sentence"

  id: Mapped[int] = mapped_column()
  document_id: Mapped[int] = mapped_column(nullable=False)
  node_id: Mapped[int] = mapped_column()
  content: Mapped[str] = mapped_column(nullable=False)
  embeddings: Mapped[list[float]] = mapped_column(ARRAY(Float))

  __table_args__ = (
		PrimaryKeyConstraint("id", "document_id"),
		ForeignKeyConstraint(["document_id"], ["document.id"], ondelete="CASCADE"),
		ForeignKeyConstraint(["node_id", "document_id"], ["node.id", "node.document_id"], ondelete="SET NULL"),
		Index("ix_sentence_document_id_node_id", "document_id", "node_id")
	)

  @classmethod
  async def create(
		cls,
		session: AsyncSession,
		document_id: int,
		node_id: int,
		content: str,
		embeddings: list[float]
	) -> "Sentence":
    """
		Create a new sentence record in the database.

		:param session: The database session
		:type session: Session

		:param document_id: The ID of the document
		:type document_id: int

		:param content: The content of the sentence
		:type content: str

		:param embeddings: The embeddings of the sentence
		:type embeddings: list[float]

		:return: The newly created sentence record
		:rtype: Sentence
		"""
		# Create a new sentence record.
    sentence: Sentence = cls(
      document_id=document_id,
      node_id=node_id,
      content=content,
      embeddings=embeddings
    )

    # Add the sentence record to the session and commit the transaction.
    try:
      session.add(sentence)
      await session.commit()
      await session.refresh(sentence)

      return sentence
    except Exception as e:
      await session.rollback()
      raise e
