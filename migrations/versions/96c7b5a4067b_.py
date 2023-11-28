"""empty message

Revision ID: 96c7b5a4067b
Revises: 
Create Date: 2023-11-28 14:21:30.041359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96c7b5a4067b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('modify_date', sa.DateTime(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_todo_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_todo'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    op.drop_table('user')
    # ### end Alembic commands ###