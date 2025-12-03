"""add ai recommendations table

Revision ID: 0003_add_ai_recommendations
Revises: 0002_add_weather_cache
Create Date: 2025-12-02 00:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_add_ai_recommendations'
down_revision = '0002_add_weather_cache'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ai_recommendations',
        sa.Column('id', sa.types.UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('farm_id', sa.types.UUID, nullable=True),
        sa.Column('sector_id', sa.types.UUID, nullable=True),
        sa.Column('inputs', sa.JSON(), nullable=False),
        sa.Column('results', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('ai_recommendations')
