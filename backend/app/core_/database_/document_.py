# %%
# Import the required classes, functions, and modules.
from sqlalchemy import func, select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Tuple

# %%
async def does_document_exist_(session_: AsyncSession, document_id_: int) -> bool:
  """
  Check if a document with a given ID exists in the database.

  :param session_: The database session
  :type session_: AsyncSession

  :param document_id_: The ID of the document
  :type document_id_: int

  :return: True if the document exists, False otherwise
  :rtype: bool
  """
  from ...models_ import Document

  result_: Result[Tuple[Document]] = await session_.execute(
    select(Document).filter(Document.id == document_id_)
  )
  return result_.scalars().first() is not None


async def read_max_document_id_for_user_(session_: AsyncSession, user_id_: str) -> int:
  """
	Retrieve the highest document ID for a given user.

	:param session_: The database session
	:type session_: AsyncSession

	:param user_id_: The ID of the user
	:type user_id_: str

	:return: The highest document ID for the user
	:rtype: int
	"""
  from ...models_ import Document

  result_: Result[Tuple[int]] = await session_.execute(
		select(func.max(Document.id)).filter(Document.user_id == user_id_)
	)

  max_document_id: int | None = result_.scalar()
  return max_document_id if max_document_id is not None else -1


async def create_document_(
  session_: AsyncSession,
  user_id_: str,
  name_: str,
  type_: str,
  path_: str
) -> Any:
  """
	Create a new document in the database.

	:param session_: The database session
	:type session_: AsyncSession

	:param user_id_: The ID of the user
	:type user_id_: str

	:param name_: The name of the document
	:type name_: str

	:param type_: The type of the document
	:type type_: str

	:param path_: The path of the document
	:type path_: str

	:return: The ID of the new document
	:rtype: int
	"""
  from ...models_ import Document

  max_document_id_: int = await read_max_document_id_for_user_(session_, user_id_)
  document_id_: int = max_document_id_ + 1

  document_: Document = Document(
		id=document_id_,
		user_id=user_id_,
		name=name_,
		type=type_,
		path=path_
	)
  session_.add(document_)

  await session_.commit()
  await session_.refresh(document_)

  return document_
