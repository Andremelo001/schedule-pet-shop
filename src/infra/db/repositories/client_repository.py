from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infra.db.entities.client import Client as ClientEntitie

from src.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.domain.models.client import Client
from src.dto.client_dto import ClientDTO, ClientUpdateDTO


class ClientRepository(InterfaceClientRepository):
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
        
    @classmethod
    async def update_client(cls, session: AsyncSession, id_client: str, client: ClientUpdateDTO) -> Client:

        result_client = await session.execute(select(ClientEntitie).where(ClientEntitie.id == id_client))

        new_client = result_client.scalar_one_or_none()
        
        if not new_client:
            raise Exception(f"Cliente com o {id_client} não encontrado")

        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(new_client, key, value)

        await session.commit()
        await session.refresh(new_client)

        return new_client
    
    @classmethod
    async def delete_client(cls, sesion: AsyncSession, id_client: str) -> None:

        client = await sesion.execute(select(ClientEntitie).where(ClientEntitie.id == id_client))

        delete_client = client.scalar_one_or_none()

        if not delete_client:
            raise Exception(f"Cliente com o id {id_client} não foi encontrado")
  
        await sesion.delete(delete_client)
        await sesion.commit()