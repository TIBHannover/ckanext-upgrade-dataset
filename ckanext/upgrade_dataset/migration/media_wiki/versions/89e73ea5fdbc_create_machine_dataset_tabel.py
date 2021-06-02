# encoding: utf-8
"""create_machine_dataset_tabel

Revision ID: 89e73ea5fdbc
Revises: 
Create Date: 2021-06-02 12:42:42.138826

"""
from alembic import op
from ckan.migration import skip_based_on_legacy_engine_version
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89e73ea5fdbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():    
    op.create_table(
        'package_mediawiki_link',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('package_name', sa.UnicodeText(), sa.ForeignKey('package.name'), nullable=False),
        sa.Column('url', sa.UnicodeText(), nullable=False),
        sa.Column('link_name', sa.UnicodeText()),
        sa.Column('create_at', sa.DateTime(timezone=False), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=False), nullable=False),
    )


def downgrade():
    op.drop_table('package_mediawiki_link')
