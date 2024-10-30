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
  __tablename__ = "_sentence"

  id: Mapped[int] = mapped_column()
  document_id: Mapped[int] = mapped_column(nullable=False)
  node_id: Mapped[int] = mapped_column(nullable=True)
  content: Mapped[str] = mapped_column(nullable=False)
  embeddings: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=True)

  __table_args__ = (
		PrimaryKeyConstraint("id", "document_id"),
		ForeignKeyConstraint(["document_id"], ["_document.id"], ondelete="CASCADE"),
		ForeignKeyConstraint(["node_id", "document_id"], ["_node.id", "_node.document_id"], ondelete="SET NULL"),
		Index("ix_sentence_document_id_node_id", "document_id", "node_id")
	)
