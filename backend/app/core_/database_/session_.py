# %%
# Import the required libraries, modules, classes and functions.
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple

# %%
async def read_user_id_by_session_id_(session_: AsyncSession, session_id_: str) -> Optional[int]:
	"""
	Read the user ID by the session ID.

	:param session_: The database session
	:type session_: AsyncSession

	:param session_id_: The session ID
	:type session_id_: str

	:return: The user ID if the session ID is valid, None otherwise
	:rtype: Optional[int]
	"""
	from ...models_ import Session

	result_: Result[Tuple[int]] = await session_.execute(
		select(Session.userId).filter(Session.id == session_id_)
	)

	return result_.scalar()
