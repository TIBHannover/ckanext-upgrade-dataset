"""add citation to table

Revision ID: 270e1617bce1
Revises: 76562928298f
Create Date: 2021-08-04 10:56:59.717313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '270e1617bce1'
down_revision = '76562928298f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('package_publication_link', sa.Column('citation', sa.UnicodeText, nullable=True))


def downgrade():
    pass
