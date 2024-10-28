# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKeyConstraint, Index, PrimaryKeyConstraint

from ..core_.database_ import Base

# %%
class Node(Base):
  __tablename__ = "node"

  id: Mapped[int] = mapped_column()
  document_id: Mapped[int] = mapped_column(nullable=False)
  parent_id: Mapped[int] = mapped_column(nullable=True)
  topic_and_content: Mapped[str] = mapped_column(nullable=False)

  __table_args__ = (
		PrimaryKeyConstraint("id", "document_id"),
		ForeignKeyConstraint(["document_id"], ["document.id"], ondelete="CASCADE"),
		ForeignKeyConstraint(["parent_id", "document_id"], ["node.id", "node.document_id"], ondelete="CASCADE"),
		Index("ix_node_document_id_parent_id", "document_id", "parent_id")
	)

  @classmethod
  async def create(
    cls,
    session: AsyncSession,
    parent_id: int,
    document_id: int,
    topic_and_content: str
  ) -> "Node":
    """
		Create a new node record in the database.

		:param session: The database session
		:type session: Session

		:param parent_id: The ID of the parent node
		:type parent_id: int

		:param document_id: The ID of the document
		:type document_id: int

		:param topic_and_content: The topic and content of the node
		:type topic_and_content: str

		:return: The newly created node record
		:rtype: Node
		"""
		# Create a new node record.
    node: Node = cls(
      parent_id=parent_id,
      document_id=document_id,
      topic_and_content=topic_and_content
    )

    # Add the node record to the session and commit the transaction.
    try:
      session.add(node)
      await session.commit()
      await session.refresh(node)

      return node
    except Exception as e:
      await session.rollback()
      raise e
