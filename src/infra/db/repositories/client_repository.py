from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import uuid4
from src.infra.db.entities.client import Client
from src.infra.dtos.client_dto import CreateClient


class ClientRepository:
    @classmethod
    async def client_exists(cls, session: AsyncSession, cpf_client: str) -> Client:

        client = await session.execute(select(Client).where(Client.cpf == cpf_client))

        return client.scalar_one_or_none()

    @classmethod
    async def create_client(cls, session: AsyncSession, client: CreateClient) -> Client:
        """Criação de um novo cliente no banco"""
        
        try:
            new_client = Client(
                id= uuid4(),
                name= client.name,
                cpf= client.cpf,
                age= client.age,
                email= client.email,
                senha= client.senha,
                is_admin= False
            )

            session.add(new_client)
            await session.commit()
            await session.refresh(new_client)

            return new_client
        
        except Exception as exception:
            await session.rollback()
            raise exception
        



