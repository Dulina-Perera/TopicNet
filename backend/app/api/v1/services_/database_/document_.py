# %%
# Import the required classes, functions, and modules.
from sqlalchemy.orm import Session

from .....models_ import Document

# %%
def does_document_exist(session: Session, document_id: int) -> bool:
  """
  Check if a document with a given ID exists in the database.

  :param session: The database session
  :type session: Session

  :param document_id: The ID of the document
  :type document_id: int

  :return: True if the document exists, False otherwise
  :rtype: bool
  """
  return session.query(Document).filter(Document.id == document_id).count() > 0
