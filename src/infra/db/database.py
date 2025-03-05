from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from .settings.connection import DBConection

db = DBConection()

# Criar tabelas no banco de dados (assíncrono)
async def create_db_and_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

def init_db():
    return create_db_and_tables(db.engine)