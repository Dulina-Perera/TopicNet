# %%
# Import the required libraries, modules, classes, and functions.
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import Index, PrimaryKeyConstraint

from ..core_.database_ import Base

# %%
class Session(Base):
	__tablename__ = "_session"

	id: Mapped[str] = mapped_column()
	userId: Mapped[str] = mapped_column(nullable=False)
	expiresAt: Mapped[datetime] = mapped_column(nullable=False)

	__table_args__ = (
		PrimaryKeyConstraint("id"),
		Index("ix_session_userId", "userId")
	)

	@classmethod
	async def create(cls, session: AsyncSession, userId: str, expiresAt: datetime) -> "Session":
		"""
		Create a new session record in the database.

		:param session: The database session
		:type session: Session

		:param userId: The ID of the user that the session belongs to
		:type userId: str

		:param expiresAt: The date and time when the session expires
		:type expiresAt: datetime

		:return: The newly created session record
		:rtype: Session
		"""
		# Create a new session record.
		session_: Session = cls(userId=userId, expiresAt=expiresAt)

		# Add the session record to the session and commit the transaction.
		try:
			session.add(session_)
			await session.commit()
			await session.refresh(session_)

			return session_
		except Exception as e:
			await session.rollback()
			raise e
