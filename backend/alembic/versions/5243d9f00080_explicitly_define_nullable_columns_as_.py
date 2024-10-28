"""explicitly define nullable columns as nullable

Revision ID: 5243d9f00080
Revises: 4b3529eb766d
Create Date: 2024-10-28 13:14:30.805491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5243d9f00080'
down_revision: Union[str, None] = '4b3529eb766d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('node', 'parent_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('sentence', 'node_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('sentence', 'embeddings',
               existing_type=postgresql.ARRAY(sa.DOUBLE_PRECISION(precision=53)),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sentence', 'embeddings',
               existing_type=postgresql.ARRAY(sa.DOUBLE_PRECISION(precision=53)),
               nullable=False)
    op.alter_column('sentence', 'node_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('node', 'parent_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###