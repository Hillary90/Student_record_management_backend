"""Add max_score and timestamps to grades

Revision ID: grade_enhancement
Revises: 04fbfeae7f88
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = 'grade_enhancement'
down_revision = '04fbfeae7f88'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to grade table
    op.add_column('grade', sa.Column('max_score', sa.Float(), default=100.0))
    op.add_column('grade', sa.Column('created_at', sa.DateTime(), default=datetime.utcnow))
    op.add_column('grade', sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow))
    
    # Update subject column length
    op.alter_column('grade', 'subject', type_=sa.String(100))

def downgrade():
    op.drop_column('grade', 'updated_at')
    op.drop_column('grade', 'created_at')
    op.drop_column('grade', 'max_score')
    op.alter_column('grade', 'subject', type_=sa.String(50))