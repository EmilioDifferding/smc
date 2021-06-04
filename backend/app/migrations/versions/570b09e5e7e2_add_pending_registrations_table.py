"""add pending_registrations table

Revision ID: 570b09e5e7e2
Revises: d3d7b35128d1
Create Date: 2021-05-30 19:03:36.121099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '570b09e5e7e2'
down_revision = 'd3d7b35128d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pending_registrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('telegram_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_pending_registrations_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pending_registrations'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pending_registrations')
    # ### end Alembic commands ###
