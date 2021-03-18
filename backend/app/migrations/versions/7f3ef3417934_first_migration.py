"""first migration

Revision ID: 7f3ef3417934
Revises: 
Create Date: 2021-03-15 16:52:37.813992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f3ef3417934'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_places'))
    )
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_places_name'), ['name'], unique=False)

    op.create_table('units',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_units'))
    )
    op.create_table('devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('unic_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_devices_place_id_places')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_devices'))
    )
    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_devices_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_devices_unic_id'), ['unic_id'], unique=True)

    op.create_table('aliases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unit_id', sa.Integer(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('max_limit', sa.Float(), nullable=True),
    sa.Column('min_limit', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name=op.f('fk_aliases_device_id_devices')),
    sa.ForeignKeyConstraint(['unit_id'], ['units.id'], name=op.f('fk_aliases_unit_id_units')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_aliases'))
    )
    op.create_table('measurements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name=op.f('fk_measurements_device_id_devices')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_measurements'))
    )
    op.create_table('values',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('measurement_id', sa.Integer(), nullable=True),
    sa.Column('alias_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['alias_id'], ['aliases.id'], name=op.f('fk_values_alias_id_aliases')),
    sa.ForeignKeyConstraint(['measurement_id'], ['measurements.id'], name=op.f('fk_values_measurement_id_measurements')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_values'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('values')
    op.drop_table('measurements')
    op.drop_table('aliases')
    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_devices_unic_id'))
        batch_op.drop_index(batch_op.f('ix_devices_name'))

    op.drop_table('devices')
    op.drop_table('units')
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_places_name'))

    op.drop_table('places')
    # ### end Alembic commands ###