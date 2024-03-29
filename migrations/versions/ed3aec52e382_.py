"""empty message

Revision ID: ed3aec52e382
Revises: 291880d88df3
Create Date: 2023-05-07 18:13:52.831052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed3aec52e382'
down_revision = '291880d88df3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artist_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('venue_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'venues', ['venue_id'], ['id'])
        batch_op.create_foreign_key(None, 'artists', ['artist_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('venue_id')
        batch_op.drop_column('artist_id')

    # ### end Alembic commands ###
