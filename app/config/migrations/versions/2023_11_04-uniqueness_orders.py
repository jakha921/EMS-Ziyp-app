"""uniqueness orders

Revision ID: 8b65a5af682d
Revises: f8bcdc963dd0
Create Date: 2023-11-04 13:47:07.564464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b65a5af682d'
down_revision = 'f8bcdc963dd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_user_product', 'orders', ['user_id', 'product_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_product', 'orders', type_='unique')
    # ### end Alembic commands ###