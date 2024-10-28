# %%
# Import the required classes, functions, and modules.
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from typing import Any, List, Optional

from ...exceptions_ import SentenceDoesNotExistError

# %%
async def does_sentence_exist(session: AsyncSession, sentence_id: int, document_id: int) -> bool:
  """
	Check if a sentence with a given sentence ID and document ID exists in the database.

	:param session: The database session
	:type session: AsyncSession

	:param sentence_id: The ID of the sentence
	:type sentence_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: True if the sentence exists, False otherwise
	:rtype: bool
	"""
  from ...models_ import Sentence

  result: Result[Tuple[Sentence]] = session.execute(
    select(Sentence).filter(Sentence.id == sentence_id, Sentence.document_id == document_id)
	)
  return result.scalars().first() is not None


async def save_sentences(
  session: AsyncSession,
  sentences: List[str],
  document_id: int
) -> List[int]:
  """
  Save a list of sentences to the database.

  :param session: The database session
  :type session: AsyncSession
  :param sentences: The list of sentences
  :type sentences: List[str]
  :param document_id: The ID of the document
  :type document_id: int
  :return: The IDs of the saved sentences
  :rtype: List[int]
  """
  from ...models_ import Sentence

  sentence_records: List[Sentence] = [
    Sentence(id=index, document_id=document_id, content=sentence)
    for (index, sentence) in enumerate(sentences)
	]
  session.add_all(sentence_records)

  await session.commit()

  return [index for index in range(len(sentences))]


async def bind_sentence_to_node(
  session: AsyncSession,
  sentence_id: int,
  document_id: int,
  node_id: int
) -> Any:
  """
	Bind a sentence to a node in the database.

	:param session: The database session
	:type session: AsyncSession

	:param sentence_id: The ID of the sentence
	:type sentence_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:param node_id: The ID of the node
	:type node_id: int

	:return: The updated sentence record
	:rtype: Sentence
	"""
  from ...models_ import Sentence

 	# Retrieve the sentence record.
  result: Result[Tuple[Sentence]] = await session.execute(
		select(Sentence).filter(Sentence.id == sentence_id, Sentence.document_id == document_id)
	)
  sentence: Optional[Sentence] = result.scalars().first()
  if sentence is None:
    raise SentenceDoesNotExistError(sentence_id, document_id)

  try:
    sentence.node_id = node_id
    session.add(sentence)

    await session.commit()
    await session.refresh(sentence)

    return sentence
  except Exception as e:
    await session.rollback()
    raise e


async def read_sentences_belonging_to_node(
	session: AsyncSession,
	node_id: int,
	document_id: int,
) -> List[Any]:
	"""
	Read the sentences that belong to the specified node.

	:param session: The database session
	:type session: AsyncSession

	:param node_id: The ID of the node
	:type node_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: A list of Sentence objects
	:rtype: List[Any]
	"""
	from ...models_ import Sentence

	result: Result[Tuple[Sentence]] = await session.execute(
		select(Sentence).filter(Sentence.node_id == node_id, Sentence.document_id == document_id)
	)
	return result.scalars().all()


async def point_sentences_to_parent_node(
	session: AsyncSession,
	node_ids: List[int],
	parent_node_id: int,
	document_id: int,
) -> None:
	"""
	Point the sentences that belong to the specified nodes to the specified parent node.

	:param session: The database session
	:type session: AsyncSession

	:param node_ids: The IDs of the nodes
	:type node_ids: List[int]

	:param parent_node_id: The ID of the parent node
	:type parent_node_id: int

	:param document_id: The ID of the document
	:type document_id: int

	:return: The updated sentence records
	:rtype: Any
	"""
	from ...models_ import Sentence

	result: Result[Tuple[Sentence]] = await session.execute(
		select(Sentence).filter(Sentence.node_id.in_(node_ids), Sentence.document_id == document_id)
	)
	sentences: List[Sentence] = result.scalars().all()

	for sentence in sentences:
		sentence.node_id = parent_node_id
		session.add(sentence)

	await session.commit()
