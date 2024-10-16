# %%
# Import the required classes, functions, and modules.
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from typing import Any, Optional

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


async def bind_sentence_to_node(session: AsyncSession, sentence_id: int, document_id: int, node_id: int) -> Any:
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
  result: Result[Tuple[Sentence]] = session.execute(
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
