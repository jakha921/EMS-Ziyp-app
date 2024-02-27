"""add completed profile to user

Revision ID: 98ae4fe07058
Revises: 172013117e71
Create Date: 2024-02-27 20:26:54.882149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98ae4fe07058'
down_revision = '172013117e71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_completed_profile', sa.Boolean(), nullable=True, comment='If user completed profile or not'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_completed_profile')
    # ### end Alembic commands ###
