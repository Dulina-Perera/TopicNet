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
