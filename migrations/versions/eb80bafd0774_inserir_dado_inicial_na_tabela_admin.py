"""inserir dado inicial na tabela admin

Revision ID: eb80bafd0774
Revises: 
Create Date: 2025-08-13 18:35:53.749710

"""
from alembic import op
import sqlalchemy as sa
import uuid
from dotenv import load_dotenv
import os 
from src.drivers.password_hasher.password_hasher import PasswordHasher

revision = "eb80bafd0774"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Criar instância do hasher
    hasher = PasswordHasher()

    # Gerar UUID e senha
    user_id = str(uuid.uuid4())

    # Carregar variáveis do .env
    load_dotenv()

    senha_plana = os.getenv("SENHA_ADMIN")

    senha_hash = hasher.hash(senha_plana)

    # Inserir no banco
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            INSERT INTO admin (id, name, senha, "user")
            VALUES (:id, :name, :senha, :user)
        """),
        {
            "id": user_id,
            "name": "Administrador",
            "senha": senha_hash,
            "user": "admin"
        }
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text('DELETE FROM admin WHERE "user" = :user'),
        {"user": "admin"}
    )

