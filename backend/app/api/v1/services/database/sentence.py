# %%
# Import the required classes, functions, and modules.
from sqlalchemy.orm import Session

from .....models import Sentence

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
