# %%
# Import the required classes, functions, and modules.
from sqlalchemy import Result, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Optional, Tuple

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


async def get_max_node_id_for_document(
  session: AsyncSession,
  document_id: int
) -> Optional[int]:
  """
  Retrieve the highest node ID for a given document.

  :param session: The database session
  :type session: AsyncSession

  :param document_id: The ID of the document
  :type document_id: int

  :return: The highest node ID for the document, or None if no nodes are found
  :rtype: Optional[int]
  """
  from ...models_ import Node

  result: Result[Tuple[int]] = await session.execute(
    select(func.max(Node.id)).filter(Node.document_id == document_id)
  )

  return result.scalar()


async def get_nodes(session: AsyncSession, document_id: int) -> List[Any]:
  """
  Read the nodes for the given document.

  :param session: The database session
  :type session: AsyncSession

  :param document_id: The ID of the document
  :type document_id: int

  :return: A list of Node objects
  :rtype: List[Any]
  """
  from ...models_ import Node

  result: Result = await session.execute(
    select(Node).filter(Node.document_id == document_id)
  )
  return result.scalars().all()


async def get_nodes_by_ids(session: AsyncSession, node_ids: List[int], document_id: int) -> List[Any]:
	"""
	Read the nodes with the specified IDs for the given document.

	:param session: The database session
	:type session: AsyncSession

	:param node_ids: The IDs of the nodes
	:type node_ids: List[int]

	:param document_id: The ID of the document
	:type document_id: int

	:return: A list of Node objects
	:rtype: List[Any]
	"""
	from ...models_ import Node

	result: Result = await session.execute(
		select(Node).filter(Node.id.in_(node_ids), Node.document_id == document_id)
	)
	return result.scalars().all()


async def save_base_nodes(
  session: AsyncSession,
  topics_and_content: List[str],
  document_id: int
) -> List[int]:
  """
	Save the base nodes for the given document.

	:param session: The database session
	:type session: AsyncSession

	:param topics_and_content: The topics and content of the nodes
	:type topics_and_content: List[str]

	:param document_id: The ID of the document
	:type document_id: int

	:return: The IDs of the saved nodes
	:rtype: List[int]
  """
  from ...models_ import Node

  root_node: Node = Node(id=0, document_id=document_id, topic_and_content=topics_and_content[0])
  node_records: List[Node] = [
    Node(id=index + 1, document_id=document_id, parent_id=0, topic_and_content=topic_and_content)
		for (index, topic_and_content) in enumerate(topics_and_content[1:])
	]
  node_records.insert(0, root_node)
  session.add_all(node_records)

  await session.commit()

  return [index for index in range(len(node_records))]


async def save_node_layer(
  session: AsyncSession,
  topics_and_content: List[str],
  parent_id: int,
  document_id: int
) -> List[int]:
  """
	Save a layer of nodes for the given document.

	:param session: The database session
	:type session: AsyncSession

	:param topics_and_content: The topics and content of the nodes
	:type topics_and_content: List[str]

	:param parent_id: The ID of the parent node
	:type parent_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: The IDs of the saved nodes
	:rtype: List[int]
  """
  from ...models_ import Node

  max_node_id: int = await get_max_node_id_for_document(session, document_id)
  node_records: List[Node] = [
		Node(id=max_node_id + index + 1, document_id=document_id, parent_id=parent_id, topic_and_content=topic_and_content)
		for (index, topic_and_content) in enumerate(topics_and_content)
	]
  session.add_all(node_records)

  await session.commit()

  return [max_node_id + index + 1 for index in range(len(node_records))]


async def has_child_nodes(session: AsyncSession, node_id: int, document_id: int) -> bool:
  """
	Check if a node has child nodes.

	:param session: The database session
	:type session: AsyncSession

	:param node_id: The ID of the node
	:type node_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: True if the node has child nodes, False otherwise
	:rtype: bool
	"""
  from ...models_ import Node

  result: Result[Tuple[Node]] = await session.execute(
    select(Node).filter(Node.parent_id == node_id, Node.document_id == document_id)
	)
  return result.scalars().first() is not None


async def read_descendant_node_ids(
  session: AsyncSession,
  node_id: int,
  document_id: int
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
