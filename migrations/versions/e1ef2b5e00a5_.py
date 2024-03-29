"""empty message

Revision ID: e1ef2b5e00a5
Revises: ed3aec52e382
Create Date: 2023-05-07 18:28:11.029579

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e1ef2b5e00a5'
down_revision = 'ed3aec52e382'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', sa.DateTime(), nullable=False))
        batch_op.drop_column('show_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('show_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('start_time')

    # ### end Alembic commands ###
