"""empty message

Revision ID: 235820e23bed
Revises: 
Create Date: 2021-05-08 22:00:42.647859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '235820e23bed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supermarket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('market_name', sa.String(length=60), nullable=False),
    sa.Column('location', sa.String(length=60), nullable=False),
    sa.Column('information', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('location', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=60), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('market_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['market_id'], ['supermarket.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_name')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coupons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coupon_name', sa.String(length=40), nullable=False),
    sa.Column('coupon_info', sa.String(length=100), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('market_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['market_id'], ['supermarket.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('couponlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('coupon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['coupon_id'], ['coupons.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('couponlist')
    op.drop_table('coupons')
    op.drop_table('cart')
    op.drop_table('product')
    op.drop_table('user')
    op.drop_table('supermarket')
    # ### end Alembic commands ###
