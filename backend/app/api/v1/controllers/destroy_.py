# %%
# Import the required libraries, modules, classes and functions.
from fastapi import APIRouter
from typing import Any

from ..services_ import does_document_exist, does_node_exist
from ....exceptions import DocumentDoesNotExistError, NodeDoesNotExistError

# %%
# Create a router for the `destroy` endpoint.
destroy_router: APIRouter = APIRouter()

# %%
@destroy_router.delete("/")
async def destroy_descendant_nodes(document_id: int, node_id: int) -> Any:
  """
	Destroy the descendant nodes of the specified node in the specified document.

	:param document_id: The ID of the document
	:type document_id: int

	:param node_id: The ID of the node
	:type node_id: int

	:return Any: The response
	:rtype: Any
	"""
  # Check if a document with the given `document_id` exists.
  if not does_document_exist(document_id):
    raise DocumentDoesNotExistError(document_id)
