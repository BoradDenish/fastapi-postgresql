"""empty message

Revision ID: 7c17d6dc329b
Revises: 916bad8c7b75
Create Date: 2024-10-24 22:01:07.502721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c17d6dc329b'
down_revision: Union[str, None] = '916bad8c7b75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_session',
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('session_email', sa.String(length=255), nullable=True),
    sa.Column('session_token', sa.String(length=955), nullable=True),
    sa.Column('session_user', sa.Integer(), nullable=True),
    sa.Column('session_expiry', sa.DateTime(), nullable=True),
    sa.Column('session_status', sa.Boolean(), nullable=True),
    sa.Column('deleted_at', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['session_user'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_index(op.f('ix_user_session_session_id'), 'user_session', ['session_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_session_session_id'), table_name='user_session')
    op.drop_table('user_session')
    # ### end Alembic commands ###