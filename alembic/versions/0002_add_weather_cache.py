"""add weather cache

Revision ID: 0002_add_weather_cache
Revises: 0001_initial
Create Date: 2025-12-02 00:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_weather_cache'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'weather_cache',
        sa.Column('id', sa.types.UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('location_hash', sa.String(), nullable=False),
        sa.Column('lat', sa.Float(), nullable=False),
        sa.Column('lon', sa.Float(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('cached_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index(op.f('ix_weather_cache_location_hash'), 'weather_cache', ['location_hash'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_weather_cache_location_hash'), table_name='weather_cache')
    op.drop_table('weather_cache')
