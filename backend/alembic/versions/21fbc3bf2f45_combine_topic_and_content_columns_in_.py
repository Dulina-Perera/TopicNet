"""combine topic and content columns in the Node model as topic_and_content

Revision ID: 21fbc3bf2f45
Revises: dc1511c44ccd
Create Date: 2024-10-14 17:05:53.971973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21fbc3bf2f45'
down_revision: Union[str, None] = 'dc1511c44ccd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('node', sa.Column('topic_and_content', sa.String(), nullable=True))
    op.drop_index('ix_node_topic', table_name='node')
    op.drop_column('node', 'content')
    op.drop_column('node', 'topic')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('node', sa.Column('topic', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_node_topic', 'node', ['topic'], unique=False)
    op.drop_column('node', 'topic_and_content')
    # ### end Alembic commands ###