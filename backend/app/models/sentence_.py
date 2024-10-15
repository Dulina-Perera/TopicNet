# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session
from sqlalchemy.schema import ForeignKeyConstraint, Index, PrimaryKeyConstraint

from ..core.database import Base

# %%
class Sentence(Base):
  __tablename__ = "sentence"

  id = Column(type_=Integer, primary_key=True)
  document_id = Column(
		ForeignKey("document.id"),
		type_=Integer,
		nullable=False,
		primary_key=True
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

  __table_args__ = (
		PrimaryKeyConstraint("id", "document_id"),
		ForeignKeyConstraint(["document_id"], ["document.id"], ondelete="CASCADE"),
		ForeignKeyConstraint(["node_id", "document_id"], ["node.id", "node.document_id"], ondelete="SET NULL"),
		Index("ix_sentence_document_id_node_id", "document_id", "node_id")
	)

  @classmethod
  def create(
		cls,
		session: Session,
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
      session.commit()

      return sentence
    except Exception as e:
      session.rollback()
      raise e
