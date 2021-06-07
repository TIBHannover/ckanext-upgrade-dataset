"""rename_package_mediawiki_link_table

Revision ID: 592b11439b7b
Revises: 8c1828835144
Create Date: 2021-06-07 10:55:25.463787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '592b11439b7b'
down_revision = '8c1828835144'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('package_mediawiki_link', 'resource_mediawiki_link')


def downgrade():
    op.rename_table('resource_mediawiki_link', 'package_mediawiki_link')
