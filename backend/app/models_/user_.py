# %%
# Import the required libraries, modules, classes, and functions.
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import Index, PrimaryKeyConstraint

from ..core_.database_ import Base

# %%
class User(Base):
	__tablename__ = "_user"

	id: Mapped[str] = mapped_column()
	username: Mapped[str] = mapped_column(nullable=False, unique=True)
	passwordHash: Mapped[str] = mapped_column(nullable=False)
	isPermanent: Mapped[bool] = mapped_column(nullable=False, default=False)

	__table_args__ = (
		PrimaryKeyConstraint("id"),
		Index("ix_user_username", "username")
	)

	@classmethod
	async def create(cls, session: AsyncSession, username: str, passwordHash: str, isPermanent: bool = False) -> "User":
		"""
		Create a new user record in the database.

		:param session: The database session
		:type session: Session

		:param username: The username of the user
		:type username: str

		:param passwordHash: The hashed password of the user
		:type passwordHash: str

		:param isPermanent: Whether the user is permanent or not
		:type isPermanent: bool

		:return: The newly created user record
		:rtype: User
		"""
		# Create a new user record.
		user: User = cls(username=username, passwordHash=passwordHash, isPermanent=isPermanent)

		# Add the user record to the session and commit the transaction.
		try:
			session.add(user)
			await session.commit()
			await session.refresh(user)

			return user
		except Exception as e:
			await session.rollback()
			raise e
