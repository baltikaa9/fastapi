"""add password to users

Revision ID: 04457c3b1d44
Revises: 52c1a4b87a2c
Create Date: 2023-06-19 12:08:02.408982

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "04457c3b1d44"
down_revision = "52c1a4b87a2c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("hashed_password", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "hashed_password")
    # ### end Alembic commands ###
