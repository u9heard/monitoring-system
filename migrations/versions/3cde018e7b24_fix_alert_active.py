"""Fix alert_active

Revision ID: 3cde018e7b24
Revises: 6f592dc3095c
Create Date: 2023-05-06 23:27:23.923560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cde018e7b24'
down_revision = '6f592dc3095c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('box', 'alert_active',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('box', 'alert_active',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###