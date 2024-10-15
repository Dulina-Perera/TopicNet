# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.schema import ForeignKeyConstraint, Index, PrimaryKeyConstraint

from ..core import Base

# %%
class Node(Base):
  __tablename__ = "node"

  id = Column(type_=Integer, autoincrement="auto", primary_key=True)
  document_id = Column(type_=Integer, nullable=False, primary_key=True)
  parent_id = Column(type_=Integer)
  topic_and_content = Column(type_=String)

  __table_args__ = (
		PrimaryKeyConstraint("id", "document_id"),
		ForeignKeyConstraint(["document_id"], ["document.id"], ondelete="CASCADE"),
		ForeignKeyConstraint(["parent_id", "document_id"], ["node.id", "node.document_id"], ondelete="CASCADE"),
		Index("ix_node_document_id_parent_id", "document_id", "parent_id")
	)

  @classmethod
  def create(
    cls,
    session: Session,
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
      session.commit()
      session.refresh(node)

      return node
    except Exception as e:
      session.rollback()
      raise e
