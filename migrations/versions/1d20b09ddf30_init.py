"""init

Revision ID: 1d20b09ddf30
Revises: 
Create Date: 2023-04-02 18:07:33.726562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d20b09ddf30'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('path', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('fcmtoken', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('box',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('id_device', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_device'], ['device.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_device')
    )
    op.create_index(op.f('ix_box_name'), 'box', ['name'], unique=True)
    op.create_table('indication',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_box', sa.Integer(), nullable=True),
    sa.Column('temp', sa.Float(), nullable=True),
    sa.Column('hum', sa.Float(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_box'], ['box.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('indication')
    op.drop_index(op.f('ix_box_name'), table_name='box')
    op.drop_table('box')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('log')
    op.drop_table('device')
    # ### end Alembic commands ###