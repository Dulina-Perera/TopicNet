# %%
# Import the required classes, functions, and modules.
from sqlalchemy.orm import Session
from typing import Optional

from .....models_ import Sentence

# %%
def does_sentence_exist(session: Session, sentence_id: int, document_id: int) -> bool:
  """
	Check if a sentence with a given sentence ID and document ID exists in the database.

	:param session: The database session
	:type session: Session

	:param sentence_id: The ID of the sentence
	:type sentence_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: True if the sentence exists, False otherwise
	:rtype: bool
	"""
  return session.query(Sentence).filter(Sentence.id == sentence_id, Sentence.document_id == document_id).count() > 0


def bind_sentence_to_node(session: Session, sentence_id: int, node_id: int) -> Sentence:
  """
	Bind a sentence to a node in the database.

	:param sentence_id: The ID of the sentence
	:type sentence_id: int

	:param node_id: The ID of the node
	:type node_id: int

	:param session: The database session
	:type session: Session

	:return: The updated sentence record
	:rtype: Sentence
	"""
	# Retrieve the sentence record.
  sentence: Optional[Sentence] = session.query(Sentence).filter(Sentence.id == sentence_id).first()

  # Update the sentence record.
  sentence.node_id = node_id

  try:
    # Commit the transaction.
    session.commit()

    # Return the updated sentence record.
    return sentence
  except Exception as e:
    # Rollback the transaction.
    session.rollback()
    raise e
