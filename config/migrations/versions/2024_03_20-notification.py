"""notification

Revision ID: 584a04b8178d
Revises: b6044a5cc6fb
Create Date: 2024-03-20 12:08:09.666307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '584a04b8178d'
down_revision = 'b6044a5cc6fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('title_ru', sa.String(length=255), nullable=False),
    sa.Column('title_uz', sa.String(length=255), nullable=True),
    sa.Column('title_en', sa.String(length=255), nullable=True),
    sa.Column('body_ru', sa.String(length=4000), nullable=True),
    sa.Column('body_en', sa.String(length=4000), nullable=True),
    sa.Column('body_uz', sa.String(length=4000), nullable=True),
    sa.Column('datetime_to_send', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###