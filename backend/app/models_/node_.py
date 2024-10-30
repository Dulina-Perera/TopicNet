# %%
# Import the required classes, functions, and modules.
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKeyConstraint, Index, PrimaryKeyConstraint

from ..core_.database_ import Base

# %%
class Node(Base):
  __tablename__ = "_node"

  id: Mapped[int] = mapped_column()
  document_id: Mapped[int] = mapped_column(nullable=False)
  parent_id: Mapped[int] = mapped_column(nullable=True)
  topic_and_content: Mapped[str] = mapped_column(nullable=False)

  __table_args__ = (
		PrimaryKeyConstraint("id", "document_id"),
		ForeignKeyConstraint(["document_id"], ["_document.id"], ondelete="CASCADE"),
		ForeignKeyConstraint(["parent_id", "document_id"], ["_node.id", "_node.document_id"], ondelete="CASCADE"),
		Index("ix_node_document_id_parent_id", "document_id", "parent_id")
	)
