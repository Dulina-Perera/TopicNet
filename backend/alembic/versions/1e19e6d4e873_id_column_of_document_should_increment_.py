"""'id' column of 'Document' should increment automatically

Revision ID: 1e19e6d4e873
Revises: 10d7305c4979
Create Date: 2024-10-31 01:29:36.925049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e19e6d4e873'
down_revision: Union[str, None] = '10d7305c4979'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
