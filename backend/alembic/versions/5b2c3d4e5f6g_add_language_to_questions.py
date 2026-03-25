"""add_language_to_questions

Revision ID: 5b2c3d4e5f6g
Revises: 4a1b2c3d4e5f
Create Date: 2026-01-25 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5b2c3d4e5f6g'
down_revision = '4a1b2c3d4e5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add language column to mock_test_questions
    op.add_column('mock_test_questions', sa.Column('language', sa.String(), nullable=True, server_default='python'))


def downgrade() -> None:
    op.drop_column('mock_test_questions', 'language')
