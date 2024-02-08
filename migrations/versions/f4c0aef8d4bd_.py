"""empty message

Revision ID: f4c0aef8d4bd
Revises: 61da14a253e8
Create Date: 2024-02-08 20:43:58.682449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4c0aef8d4bd'
down_revision = '61da14a253e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complaints', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo', sa.String(length=255), nullable=False))
        batch_op.drop_column('photo_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complaints', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo_url', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.drop_column('photo')

    # ### end Alembic commands ###
