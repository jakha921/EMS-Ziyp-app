"""add to user work

Revision ID: 0e9ade249bce
Revises: be256889ccc7
Create Date: 2023-12-07 15:58:55.065835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e9ade249bce'
down_revision = 'be256889ccc7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('work_in', sa.String(length=255), nullable=True, comment='Need to add where user is work'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'work_in')
    # ### end Alembic commands ###
