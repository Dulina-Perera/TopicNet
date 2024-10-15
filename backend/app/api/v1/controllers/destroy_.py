# %%
# Import the required libraries, modules, classes and functions.
from fastapi import APIRouter, Depends
from logging import Logger
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session
from typing import Any

from ....core_ import does_document_exist, does_node_exist, get_db_session, get_logger
from ....exceptions_ import DocumentDoesNotExistError, NodeDoesNotExistError

# %%
# Create a router for the `destroy` endpoint.
destroy_router: APIRouter = APIRouter()

# %%
@destroy_router.delete("/")
async def destroy_descendant_nodes(
  document_id: int,
  node_id: int,
  db_session: scoped_session[Session] = Depends(get_db_session),
  logger: Logger = Depends(get_logger)
) -> Any:
  """
	Destroy the descendant nodes of the specified node in the specified document.

	:param document_id: The ID of the document
	:type document_id: int

	:param node_id: The ID of the node
	:type node_id: int

	:return Any: The response
	:rtype: Any
	"""
  try:
    # Check if a document with the given `document_id` exists.
    if not does_document_exist(db_session, document_id):
      raise DocumentDoesNotExistError(document_id)
    # Check if a node with the given `node_id` exists.
    if not does_node_exist(db_session, node_id, document_id):
      raise NodeDoesNotExistError(node_id)
  except Exception as e:
    pass
