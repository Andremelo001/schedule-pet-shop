from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.infra.db.entities.client import Client as ClientEntitie
from src.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.domain.models.client import Client
from src.dto.client_dto import ClientDTO


class ClientRepository(InterfaceClientRepository):
    @classmethod
    async def get_client(cls, session: AsyncSession, cpf_client: str) -> Client:
        """Buscando um cliente pelo seu CPF"""

        client = await session.execute(select(ClientEntitie).where(ClientEntitie.cpf == cpf_client))

        return client.scalar_one_or_none()

    @classmethod
    async def create_client(cls, session: AsyncSession, client: ClientDTO) -> None:
        """Criação de um novo cliente no banco"""
        
        try:
            new_client = ClientEntitie(
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
        
        except Exception as exception:
            await session.rollback()
            raise exception
        



