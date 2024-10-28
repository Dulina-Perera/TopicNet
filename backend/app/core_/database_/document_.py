# %%
# Import the required classes, functions, and modules.
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple

# %%
async def does_document_exist(session: AsyncSession, document_id: int) -> bool:
  """
  Check if a document with a given ID exists in the database.

  :param session: The database session
  :type session: AsyncSession

  :param document_id: The ID of the document
  :type document_id: int

  :return: True if the document exists, False otherwise
  :rtype: bool
  """
  from ...models_ import Document

  result: Result[Tuple[Document]] = await session.execute(
    select(Document).filter(Document.id == document_id)
  )
  return result.scalars().first() is not None


async def save_s3_uri(session: AsyncSession, s3_uri: str) -> int:
	"""
	Save the S3 URI of a document in the database.

	:param session: The database session
	:type session: AsyncSession

	:param s3_uri: The S3 URI of the document
	:type s3_uri: str

	:return: The ID of the document
	:rtype: int
	"""
	from ...models_ import Document

	document: Document = await Document.create(session, s3_uri)
	return document.id
