"""'stable'

Revision ID: 17a1c823f23d
Revises: 
Create Date: 2020-09-29 19:06:05.604417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17a1c823f23d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fmw',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('fmd_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fmd_id'], ['unit.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personnel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('rank', sa.Text(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('fmw_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fmw_id'], ['fmw.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('clearance', sa.Integer(), nullable=False),
    sa.Column('fmw_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fmw_id'], ['fmw.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personnel_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('am_status', sa.Text(), nullable=True),
    sa.Column('am_remarks', sa.Text(), nullable=True),
    sa.Column('pm_status', sa.Text(), nullable=True),
    sa.Column('pm_remarks', sa.Text(), nullable=True),
    sa.Column('personnel_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['personnel_id'], ['personnel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('personnel_status')
    op.drop_table('user')
    op.drop_table('personnel')
    op.drop_table('fmw')
    op.drop_table('unit')
    # ### end Alembic commands ###
