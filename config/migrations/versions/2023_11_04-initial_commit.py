"""initial commit

Revision ID: 53610a110db0
Revises: 
Create Date: 2023-11-04 11:37:38.836215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53610a110db0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_uz', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=4000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_uz', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('faqs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_uz', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('description_ru', sa.String(length=4000), nullable=True),
    sa.Column('description_en', sa.String(length=4000), nullable=True),
    sa.Column('description_uz', sa.String(length=4000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_uz', sa.String(length=255), nullable=False),
    sa.Column('description_ru', sa.String(length=4000), nullable=True),
    sa.Column('description_en', sa.String(length=4000), nullable=True),
    sa.Column('description_uz', sa.String(length=4000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True, comment='Image url'),
    sa.Column('form_link', sa.String(), nullable=True, comment='Link to registration form'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_uz', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('description_ru', sa.String(length=4000), nullable=True),
    sa.Column('description_en', sa.String(length=4000), nullable=True),
    sa.Column('description_uz', sa.String(length=4000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_uz', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('is_paid_event', sa.Boolean(), nullable=False),
    sa.Column('place', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('scores', sa.Integer(), nullable=False),
    sa.Column('image_urls', sa.String(), nullable=False),
    sa.Column('description_ru', sa.String(length=4000), nullable=True),
    sa.Column('description_en', sa.String(length=4000), nullable=True),
    sa.Column('description_uz', sa.String(length=4000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_uz', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('description_ru', sa.String(length=4000), nullable=True),
    sa.Column('description_en', sa.String(length=4000), nullable=True),
    sa.Column('description_uz', sa.String(length=4000), nullable=True),
    sa.Column('images', sa.String(), nullable=True, comment='Array of image urls'),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('middle_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.Enum('admin', 'user', 'master', name='role'), nullable=False, comment='Static 3 roles as user, admin and master'),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('study_in', sa.String(length=255), nullable=True, comment='Need to add where user is study'),
    sa.Column('additional_data', sa.String(length=4000), nullable=True),
    sa.Column('avatar_url', sa.String(length=1000), nullable=True),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('application_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='status'), nullable=False),
    sa.Column('description', sa.String(length=4000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application_grands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('grand_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='status'), nullable=False),
    sa.Column('description', sa.String(length=4000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['grand_id'], ['grands.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('volunteers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('volunteers')
    op.drop_table('orders')
    op.drop_table('application_grands')
    op.drop_table('application_events')
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('events')
    op.drop_table('news')
    op.drop_table('grands')
    op.drop_table('faqs')
    op.drop_table('cities')
    op.drop_table('categories')
    # ### end Alembic commands ###