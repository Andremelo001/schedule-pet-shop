from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.infra.db.settings.connection import DBConection

from src.infra.db.entities.client import Client
from src.infra.db.entities.pet import Pet
from src.infra.db.entities.schedule import Schedule
from src.infra.db.entities.services import Services
from src.infra.db.entities.admin import Admin

db = DBConection()

# Criar tabelas no banco de dados (assíncrono)
async def create_db_and_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def init_db():
    await create_db_and_tables(db.engine)