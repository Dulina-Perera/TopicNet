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
