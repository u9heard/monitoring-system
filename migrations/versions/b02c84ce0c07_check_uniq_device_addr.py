"""check uniq device addr

Revision ID: b02c84ce0c07
Revises: 1d20b09ddf30
Create Date: 2023-04-11 21:33:07.746680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b02c84ce0c07'
down_revision = '1d20b09ddf30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('box_id_device_key', 'box', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('box_id_device_key', 'box', ['id_device'])
    # ### end Alembic commands ###
