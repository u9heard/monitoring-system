"""Delete alert_active

Revision ID: 45be53393612
Revises: 5d5ca03c6540
Create Date: 2023-05-06 23:12:44.307186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45be53393612'
down_revision = '5d5ca03c6540'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('box', 'alert_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('box', sa.Column('alert_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###