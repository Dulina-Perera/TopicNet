"""
Drop all tables.

Revision ID: 473c703c96e6
Revises: 21fbc3bf2f45
Create Date: 2024-10-15 19:13:31.778052
"""

# %%
import sqlalchemy as sa

from alembic import op
from typing import Sequence, Union

# %%
# Revision identifiers (used by Alembic)
revision: str = "473c703c96e6"
down_revision: Union[str, None] = "21fbc3bf2f45"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# %%
def upgrade() -> None:
  op.drop_table("sentence")
  op.drop_table("node")

  op.drop_index("ix_document_path", table_name="document")
  op.drop_table("document")


def downgrade() -> None:
  op.create_table(
    "document",
    sa.Column("id", sa.Integer(), autoincrement="ignore_fk", nullable=False),
    sa.Column("path", sa.String(), nullable=False),
    sa.PrimaryKeyConstraint("id")
  )
  op.create_index(op.f("ix_document_path"), "document", ["path"], unique=True)

  op.create_table("node",
    sa.Column("id", sa.Integer(), autoincrement="ignore_fk", nullable=False),
    sa.Column("parent_id", sa.Integer(), nullable=True),
    sa.Column("document_id", sa.Integer(), nullable=False),
    sa.Column('topic_and_content', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(["document_id"], ["document.id"], ),
    sa.ForeignKeyConstraint(["parent_id"], ["node.id"], ),
    sa.PrimaryKeyConstraint("id")
  )

  op.create_table("sentence",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("document_id", sa.Integer(), nullable=False),
    sa.Column("node_id", sa.Integer(), nullable=True),
    sa.Column("content", sa.String(), nullable=False),
    sa.Column("embeddings", postgresql.ARRAY(sa.Float()), nullable=True),
    sa.ForeignKeyConstraint(["document_id"], ["document.id"], ),
    sa.ForeignKeyConstraint(["node_id"], ["node.id"], ),
    sa.PrimaryKeyConstraint("id")
    )
