"""media meta column

Revision ID: ff823b8ec55e
Revises: 85f30b085401
Create Date: 2024-07-27 02:25:47.898392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff823b8ec55e'
down_revision: Union[str, None] = '85f30b085401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media_metadata', sa.Column('meta', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('media_metadata', 'meta')
    # ### end Alembic commands ###
