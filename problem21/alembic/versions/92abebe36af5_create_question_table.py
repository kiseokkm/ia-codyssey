"""create question table

Revision ID: 92abebe36af5
Revises: 
Create Date: 2025-12-01 18:44:02.902526
"""

from alembic import op
import sqlalchemy as sa

revision = '92abebe36af5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'question',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('subject', sa.String(200), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('create_date', sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('question')
