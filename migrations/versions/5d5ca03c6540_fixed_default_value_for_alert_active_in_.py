"""Fixed default value for alert_active in Box table again

Revision ID: 5d5ca03c6540
Revises: 1f45758fb450
Create Date: 2023-05-06 23:10:47.302819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d5ca03c6540'
down_revision = '1f45758fb450'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('box', 'alert_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('box', 'alert_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
