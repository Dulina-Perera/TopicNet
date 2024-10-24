# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple

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


async def read_descendant_node_ids(
  session: AsyncSession, node_id: int, document_id: int
) -> List[int]:
  """
  Find all descendant nodes of the specified node for the given document.

  :param session: The database session
  :type session: AsyncSession

  :param node_id: The ID of the ancestor node
  :type node_id: int

  :param document_id: The ID of the document
  :type document_id: int

  :return: A list of node IDs for all descendant nodes of the ancestor node
  :rtype: List[int]
  """
  from ...models_ import Node

  descendant_node_ids: List[int] = []
  curr_level_node_ids: List[int] = [node_id]
  next_level_node_ids: List[int] = []

  while curr_level_node_ids:
    for node_id in curr_level_node_ids:
      result: Result[Tuple[int]] = await session.execute(
      	select(Node.id).filter(Node.parent_id == node_id, Node.document_id == document_id)
    	)

      next_level_node_ids.extend(result.scalars().all())

    descendant_node_ids.extend(next_level_node_ids)
    curr_level_node_ids = next_level_node_ids
    next_level_node_ids = []

  return descendant_node_ids


async def delete_nodes(session: AsyncSession, node_ids: List[int], document_id: int) -> None:
	"""
	Delete the nodes with the specified IDs for the given document.

	:param session: The database session
	:type session: AsyncSession

	:param node_ids: The IDs of the nodes to be deleted
	:type node_ids: List[int]

	:param document_id: The ID of the document
	:type document_id: int
	"""
	from ...models_ import Node

	await session.execute(
		delete(Node).filter(Node.id.in_(node_ids), Node.document_id == document_id)
	)
	await session.commit()
