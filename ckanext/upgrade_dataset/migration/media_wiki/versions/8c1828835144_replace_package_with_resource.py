"""replace_package_with_resource

Revision ID: 8c1828835144
Revises: 89e73ea5fdbc
Create Date: 2021-06-07 10:38:49.289472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c1828835144'
down_revision = '89e73ea5fdbc'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('package_mediawiki_link', 'package_name')
    op.add_column('package_mediawiki_link', sa.Column('resource_id', sa.UnicodeText, sa.ForeignKey('resource.id'), nullable=False))


def downgrade():
    op.drop_column('package_mediawiki_link', 'resource_id')
    op.add_column('package_mediawiki_link', sa.Column('package_name', sa.UnicodeText, sa.ForeignKey('package.name'), nullable=False))

