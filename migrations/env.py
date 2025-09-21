import sys
import os
from dotenv import load_dotenv
import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

# Adiciona 'src' no path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Importa seus modelos
from src.infra.db.entities import *

# Configuração do Alembic
config = context.config

# Carregar variáveis do .env
load_dotenv()
# Carregar .env.local se existir (sobrescreve configurações para desenvolvimento local)
load_dotenv('.env.local', override=True)

database_url = os.getenv("DATABASE_URL")

config.set_main_option("sqlalchemy.url", database_url)

# Configuração de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados para autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Executa migrations no modo offline"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Executa migrations no modo online (assíncrono)"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
