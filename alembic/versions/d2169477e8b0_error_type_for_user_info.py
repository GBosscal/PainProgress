"""error type for user info

Revision ID: d2169477e8b0
Revises: 74b10cb2ca62
Create Date: 2023-09-12 11:29:00.433306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd2169477e8b0'
down_revision: Union[str, None] = '74b10cb2ca62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'user_name',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    op.alter_column('user', 'hospital_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('user', 'user_type',
               existing_type=mysql.ENUM('DOCTOR', 'PATIENT'),
               nullable=False)
    op.alter_column('user', 'age',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('user', 'wechat_id',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'wechat_id',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('user', 'age',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('user', 'user_type',
               existing_type=mysql.ENUM('DOCTOR', 'PATIENT'),
               nullable=True)
    op.alter_column('user', 'hospital_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('user', 'user_name',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    # ### end Alembic commands ###
