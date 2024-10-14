# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

from ..core.database import Base

# %%
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
  topic_and_content = Column(type_=String)

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
    node: Node = cls(parent_id, document_id, topic_and_content)

    # Add the node record to the session and commit the transaction.
    try:
      session.add(node)
      session.commit()

      return node
    except Exception as e:
      session.rollback()
      raise e
