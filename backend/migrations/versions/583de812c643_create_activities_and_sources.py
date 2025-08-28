from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '583de812c643'
down_revision = '4441aa646105'
branch_labels = None
depends_on = None

SCOPE_ENUM_NAME = 'scopeenum'
SCOPE_ENUM = postgresql.ENUM('1', '2', '3', name=SCOPE_ENUM_NAME, create_type=False)

def upgrade():
    # 1) Ensure enum exists with desired values
    op.execute(f"""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{SCOPE_ENUM_NAME}') THEN
            CREATE TYPE {SCOPE_ENUM_NAME} AS ENUM ('1','2','3');
        END IF;
    END$$;
    """)

    # 2) Create tables
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('filename', sa.String(), nullable=True),
        sa.Column('storage_uri', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sources_id', 'sources', ['id'], unique=False)
    op.create_index('ix_sources_org_id', 'sources', ['org_id'], unique=False)

    op.create_table(
        'activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=True),
        sa.Column('scope', SCOPE_ENUM, nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('unit', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('data_quality', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_activities_id', 'activities', ['id'], unique=False)
    op.create_index('ix_activities_org_id', 'activities', ['org_id'], unique=False)


def downgrade():
    # drop tables first
    op.drop_index('ix_activities_org_id', table_name='activities')
    op.drop_index('ix_activities_id', table_name='activities')
    op.drop_table('activities')

    op.drop_index('ix_sources_org_id', table_name='sources')
    op.drop_index('ix_sources_id', table_name='sources')
    op.drop_table('sources')

    # keep enum type for future use (or drop if you prefer)
    # op.execute("DROP TYPE IF EXISTS scopeenum")
