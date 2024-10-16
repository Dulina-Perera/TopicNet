# %%
# Import the required classes, functions, and modules.
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple

# %%
async def does_node_exist(session: AsyncSession, node_id: int, document_id: int) -> bool:
  """
	Check if a node with a given node ID and document ID exists in the database.

	:param session: The database session
	:type session: AsyncSession

	:param node_id: The ID of the node
	:type node_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: True if the node exists, False otherwise
	:rtype: bool
	"""
  from ...models_ import Node

  result: Result[Tuple[Node]] = await session.execute(
    select(Node).filter(Node.id == node_id, Node.document_id == document_id)
	)
  return result.scalars().first() is not None
