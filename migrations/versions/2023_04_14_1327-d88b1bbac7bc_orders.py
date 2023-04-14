"""orders

Revision ID: d88b1bbac7bc
Revises: 36994ca6d50b
Create Date: 2023-04-14 13:27:34.953473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd88b1bbac7bc'
down_revision = '36994ca6d50b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('avg_rating', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('reviews_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'reviews_count')
    op.drop_column('products', 'avg_rating')
    # ### end Alembic commands ###