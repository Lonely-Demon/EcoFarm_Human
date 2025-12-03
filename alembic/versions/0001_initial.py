"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-12-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.types.UUID, primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('supabase_id', sa.String(), nullable=False, unique=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )
    # Farms
    op.create_table(
        'farms',
        sa.Column('id', sa.types.UUID, primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.types.UUID, sa.ForeignKey('users.id')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('geom', sa.Text(), nullable=True),
        sa.Column('area_ha', sa.Float(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )
    # Sectors
    op.create_table(
        'sectors',
        sa.Column('id', sa.types.UUID, primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('farm_id', sa.types.UUID, sa.ForeignKey('farms.id')),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('geom', sa.Text(), nullable=True),
        sa.Column('crop', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('sectors')
    op.drop_table('farms')
    op.drop_table('users')
