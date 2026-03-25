"""add_violations_tracking

Revision ID: 4a1b2c3d4e5f
Revises: 3725a436c82a
Create Date: 2026-01-25 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4a1b2c3d4e5f'
down_revision = '3725a436c82a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add violations tracking to mock_test_attempts
    op.add_column('mock_test_attempts', sa.Column('violations_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('mock_test_attempts', sa.Column('violations_log', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    op.drop_column('mock_test_attempts', 'violations_log')
    op.drop_column('mock_test_attempts', 'violations_count')
