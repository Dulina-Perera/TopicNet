# %%
# Import the required libraries, modules, classes and functions.
from fastapi import APIRouter, Depends
from logging import Logger
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session
from typing import Any, List

from ....core_ import (
  delete_nodes,
  does_document_exist,
  does_node_exist,
  get_db_session,
  get_logger,
  read_descendant_node_ids
)
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
  logger.info(
    f"destroy_router.delete -> destroy_descendant_nodes: "
    f"document_id={document_id}, node_id={node_id}"
  )

  try:
    # Check if a document with the given `document_id` exists.
    if not does_document_exist(db_session, document_id):
      logger.error(f"Document {document_id} does not exist")
      raise DocumentDoesNotExistError(document_id)
    logger.info(f"Document {document_id} exists")

    # Check if a node with the given `node_id` exists.
    if not does_node_exist(db_session, node_id, document_id):
      logger.error(f"Node {node_id} does not exist for document {document_id}")
      raise NodeDoesNotExistError(node_id)
    logger.info(f"Node {node_id} exists for document {document_id}")

    # Find the IDs of all descendant nodes of the specified node.
    descendant_node_ids: List[int] = await read_descendant_node_ids(db_session, node_id, document_id)
    logger.info(f"Descendant node IDs: {descendant_node_ids}")

    # Delete the descendant nodes.
    delete_nodes(db_session, reversed(descendant_node_ids))
    logger.info(f"Deleted descendant nodes")

    return {
      "message": "Descendant nodes deleted"
    }
  except Exception as e:
    pass
