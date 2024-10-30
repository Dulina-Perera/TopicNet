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


async def read_path_for_document_owned_by_user_(session_: AsyncSession, document_id_: int) -> str:
  """
	Retrieve the path of a document owned by a user.

	:param session_: The database session
	:type session_: AsyncSession

	:param document_id_: The ID of the document
	:type document_id_: int

	:return: The path of the document
	:rtype: str
	"""
  from ...models_ import Document

  result_: Result[Tuple[str]] = await session_.execute(
		select(Document.path).filter(Document.id == document_id_)
	)

  path_: str | None = result_.scalar()
  return path_ if path_ is not None else ""


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

  document_: Document = Document(
		user_id=user_id_,
		name=name_,
		type=type_,
		path=path_
	)
  session_.add(document_)

  await session_.commit()
  await session_.refresh(document_)

  return document_
