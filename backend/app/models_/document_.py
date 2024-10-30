# %%
# Import the required classes, functions, and modules.
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKeyConstraint, Index, PrimaryKeyConstraint

from ..core_.database_ import Base

# %%
class Document(Base):
  __tablename__ = "_document"

  id: Mapped[int] = mapped_column()
  user_id: Mapped[str] = mapped_column(nullable=False)
  name: Mapped[str] = mapped_column(nullable=False)
  type: Mapped[str] = mapped_column(nullable=False)
  path: Mapped[str] = mapped_column(nullable=False, unique=True)

  __table_args__ = (
    PrimaryKeyConstraint("id", "user_id"),
    ForeignKeyConstraint(["user_id"], ["_user.id"], ondelete="CASCADE"),
    Index("ix_document_user_id", "user_id")
	)
