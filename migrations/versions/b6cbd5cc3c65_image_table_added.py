"""Image table added

Revision ID: b6cbd5cc3c65
Revises: e37eb7fb6240
Create Date: 2022-12-02 11:33:30.334706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6cbd5cc3c65'
down_revision = 'e37eb7fb6240'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_image',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.String(length=128), nullable=True),
    sa.Column('userImg', sa.Text(), nullable=True),
    sa.Column('userImg_mimetype', sa.String(length=128), nullable=True),
    sa.Column('userImg_encoded_value', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_image')
    # ### end Alembic commands ###
