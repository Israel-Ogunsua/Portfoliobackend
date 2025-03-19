"""Updated Project model

Revision ID: 67dceb41cf72
Revises: 795c499f51c2
Create Date: 2025-02-03 00:51:44.208232

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '67dceb41cf72'
down_revision = '795c499f51c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('long_description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('features', sqlite.JSON(), nullable=True))
        batch_op.add_column(sa.Column('screenshots', sqlite.JSON(), nullable=True))
        batch_op.add_column(sa.Column('tech_stack', sqlite.JSON(), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.drop_column('tech_stack')
        batch_op.drop_column('screenshots')
        batch_op.drop_column('features')
        batch_op.drop_column('long_description')

    # ### end Alembic commands ###
