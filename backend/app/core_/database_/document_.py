# %%
# Import the required classes, functions, and modules.
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple

from ...models_ import Document

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
  result: Result[Tuple[Document]] = await session.execute(
    select(Document).filter(Document.id == document_id)
  )
  return result.scalars().first() is not None
