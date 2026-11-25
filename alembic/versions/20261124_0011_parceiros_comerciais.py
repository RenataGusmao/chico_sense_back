"""Explicit ADMIN-approved carrier/partner relationships. No automatic backfill."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '20261124_0011_parceiros'
down_revision = '20261028_0010_exaustao_virtual'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('parceiros_comerciais',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('transportadora_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('empresas.id'), nullable=False),
        sa.Column('empresa_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('empresas.id'), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False),
        sa.Column('aprovado_por_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('atualizado_por_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('justificativa', sa.String(2000), nullable=False),
        sa.UniqueConstraint('transportadora_id', 'empresa_id', name='uq_parceiro_transportadora_empresa'),
        sa.CheckConstraint('transportadora_id <> empresa_id', name='ck_parceiro_empresas_distintas'),
    )
    op.create_index('ix_parceiro_transportadora_ativo', 'parceiros_comerciais', ['transportadora_id', 'ativo'])


def downgrade():
    op.drop_index('ix_parceiro_transportadora_ativo', table_name='parceiros_comerciais')
    op.drop_table('parceiros_comerciais')
