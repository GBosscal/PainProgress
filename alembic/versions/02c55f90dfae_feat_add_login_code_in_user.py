"""feat: add login code in user

Revision ID: 02c55f90dfae
Revises: 2c10aae8d6d6
Create Date: 2024-02-01 17:05:13.876559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02c55f90dfae'
down_revision: Union[str, None] = '2c10aae8d6d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('login_code', sa.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'login_code')
    # ### end Alembic commands ###