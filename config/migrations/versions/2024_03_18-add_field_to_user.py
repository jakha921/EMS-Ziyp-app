"""add field to user

Revision ID: b6044a5cc6fb
Revises: 80afd1527ebf
Create Date: 2024-03-18 10:02:54.655702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6044a5cc6fb'
down_revision = '80afd1527ebf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_volunteer', sa.Boolean(), nullable=True, comment='If user is volunteer or not'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_volunteer')
    # ### end Alembic commands ###
