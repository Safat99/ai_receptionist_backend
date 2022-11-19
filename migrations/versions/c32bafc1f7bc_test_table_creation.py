"""test table creation

Revision ID: c32bafc1f7bc
Revises: 
Create Date: 2022-11-19 05:56:23.417507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c32bafc1f7bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('uid', sa.String(length=128), nullable=False),
    sa.Column('userName', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=32), nullable=False),
    sa.Column('isVerified', sa.Boolean(), nullable=False),
    sa.Column('userImg', sa.Text(), nullable=False),
    sa.Column('userImg_mimetype', sa.Text(), nullable=False),
    sa.Column('userAudioLocation', sa.Text(), nullable=False),
    sa.Column('registeredDate', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
