from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infra.db.entities.client import Client as ClientEntitie
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.domain.models.client import Client
from src.modules.user.dto.client_dto import ClientDTO, ClientUpdateDTO

from src.errors.types_errors import HttpNotFoundError


class ClientRepository(InterfaceClientRepository):
    @classmethod
    async def get_client_by_id(cls, session: AsyncSession, id_client: str) -> Client:

        client = await session.execute(select(ClientEntitie).where(ClientEntitie.id == id_client))

        return client.scalar_one_or_none()

    @classmethod
    async def get_client(cls, session: AsyncSession, cpf_client: str) -> Client:

        client = await session.execute(select(ClientEntitie).where(ClientEntitie.cpf == cpf_client))

        return client.scalar_one_or_none()

    @classmethod
    async def create_client(cls, session: AsyncSession, client: ClientDTO) -> None:
        
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
        
    async def update_client(self, session: AsyncSession, id_client: str, client: ClientUpdateDTO) -> Client:

        new_client = await self.get_client_by_id(session, id_client)
        
        if not new_client:
            raise HttpNotFoundError(f"Cliente com o {id_client} não encontrado")

        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(new_client, key, value)

        await session.commit()
        await session.refresh(new_client)

        return new_client
    
    async def delete_client(self, session: AsyncSession, id_client: str) -> None:

        delete_client = await self.get_client_by_id(session, id_client)

        if not delete_client:
            raise HttpNotFoundError(f"Cliente com o id {id_client} não foi encontrado")
  
        await session.delete(delete_client)
        await session.commit()

    async def get_client_by_email(self, session: AsyncSession, email: str) -> Client:

        user = await session.execute(select(ClientEntitie).where(ClientEntitie.email == email))

        return user.scalar_one_or_none()
