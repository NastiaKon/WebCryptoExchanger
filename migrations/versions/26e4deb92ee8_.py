"""empty message

Revision ID: 26e4deb92ee8
Revises: 
Create Date: 2020-03-15 13:27:38.237327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26e4deb92ee8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kind_currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency_full', sa.String(length=32), nullable=False),
    sa.Column('currency_short', sa.String(length=16), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('c_course_prodaza', sa.Float(), nullable=False),
    sa.Column('c_course_pokupka', sa.Float(), nullable=False),
    sa.Column('c_course_market', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('currency_short')
    )
    op.create_index(op.f('ix_kind_currency_currency_full'), 'kind_currency', ['currency_full'], unique=True)
    op.create_table('kind_operations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('operation_full', sa.String(length=32), nullable=False),
    sa.Column('operation_short', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('operation_short')
    )
    op.create_index(op.f('ix_kind_operations_operation_full'), 'kind_operations', ['operation_full'], unique=True)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=12), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_title'), 'roles', ['title'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('bank_acc_curr', sa.String(length=20), nullable=False),
    sa.Column('balance_curr', sa.String(length=128), nullable=True),
    sa.Column('bank_acc_rubl', sa.String(length=20), nullable=False),
    sa.Column('balance_rubl', sa.String(length=128), nullable=True),
    sa.Column('descr', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bank_acc_curr'),
    sa.UniqueConstraint('bank_acc_rubl')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('sum_curr', sa.Float(), nullable=True),
    sa.Column('sum_rubl', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('operation_id', sa.Integer(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['kind_currency.id'], ),
    sa.ForeignKeyConstraint(['operation_id'], ['kind_operations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_timestamp'), 'transactions', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_timestamp'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_roles_title'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_kind_operations_operation_full'), table_name='kind_operations')
    op.drop_table('kind_operations')
    op.drop_index(op.f('ix_kind_currency_currency_full'), table_name='kind_currency')
    op.drop_table('kind_currency')
    # ### end Alembic commands ###
