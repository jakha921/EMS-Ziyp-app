"""add location to event

Revision ID: 2fbde4a8e695
Revises: d7c735af0d6a
Create Date: 2024-06-11 15:18:14.197507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fbde4a8e695'
down_revision = 'd7c735af0d6a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('events', sa.Column('longitude', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'longitude')
    op.drop_column('events', 'latitude')
    # ### end Alembic commands ###
