"""initialization

Revision ID: 76562928298f
Revises: 
Create Date: 2021-07-09 12:25:49.673003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76562928298f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
   op.create_table(
        'package_publication_link',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('package_name', sa.UnicodeText(), sa.ForeignKey('package.name'), nullable=False),
        sa.Column('doi', sa.UnicodeText(), nullable=False),        
        sa.Column('create_at', sa.DateTime(timezone=False), nullable=False),        
    )


def downgrade():
    op.drop_table('package_publication_link')
