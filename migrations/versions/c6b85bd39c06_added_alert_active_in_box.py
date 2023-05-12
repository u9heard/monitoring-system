"""Added alert_active in Box

Revision ID: c6b85bd39c06
Revises: df883ae5d6f9
Create Date: 2023-05-06 20:06:21.899796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6b85bd39c06'
down_revision = 'df883ae5d6f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('box', sa.Column('alert_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('box', 'alert_active')
    # ### end Alembic commands ###