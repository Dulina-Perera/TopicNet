# %%
# Import the required classes, functions, and modules.
from sqlalchemy.orm import Session

from .....models_ import Node

# %%
def does_node_exist(session: Session, node_id: int, document_id: int) -> bool:
  """
	Check if a node with a given node ID and document ID exists in the database.

	:param session: The database session
	:type session: Session

	:param node_id: The ID of the node
	:type node_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: True if the node exists, False otherwise
	:rtype: bool
	"""
  return session.query(Node).filter(Node.id == node_id, Node.document_id == document_id).count() > 0
