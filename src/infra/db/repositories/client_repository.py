from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from typing import List

from src.infra.db.entities.client import Client as ClientEntitie, ClientWithPetsWithSchedules
from src.infra.db.entities.schedule import Schedule

from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.domain.models.client import Client

from src.modules.user.dto.client_dto import ClientDTO, ClientUpdateDTO


class ClientRepository(InterfaceClientRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_client_by_id(self, id_client: str) -> Client:

        client = await self.__session.execute(select(ClientEntitie).where(ClientEntitie.id == id_client))

        return client.scalar_one_or_none()

    async def get_client(self, cpf_client: str) -> Client:

        client = await self.__session.execute(select(ClientEntitie).where(ClientEntitie.cpf == cpf_client))

        return client.scalar_one_or_none()

    async def create_client(self, client: ClientDTO) -> None:
        
        try:
            new_client = ClientEntitie(
                id= uuid4(),
                name= client.name,
                cpf= client.cpf,
                age= client.age,
                email= client.email,
                senha= client.senha,
            )

            self.__session.add(new_client)
            await self.__session.commit()
            await self.__session.refresh(new_client)
        
        except Exception as exception:
            await self.__session.rollback()
            raise exception
        
    async def update_client(self, id_client: str, client: ClientUpdateDTO) -> Client:

        new_client = (await self.__session.execute(select(ClientEntitie).where(ClientEntitie.id == id_client))).scalar_one_or_none()

        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(new_client, key, value)

        await self.__session.commit()
        await self.__session.refresh(new_client)

        return new_client
    
    async def delete_client(self, id_client: str) -> None:

        client = (await self.__session.execute(select(ClientEntitie).where(ClientEntitie.id == id_client))).scalar_one_or_none()

        await self.__session.delete(client)
        await self.__session.commit()

    async def get_client_by_email(self, email: str) -> Client:

        user = await self.__session.execute(select(ClientEntitie).where(ClientEntitie.email == email))

        return user.scalar_one_or_none()
    
    async def get_client_with_pets_and_schedules_by_id(self, id_client: str) -> ClientWithPetsWithSchedules:

        client = (await self.__session.execute(select(ClientEntitie).options(selectinload(ClientEntitie.pets), selectinload(ClientEntitie.schedules)).where(ClientEntitie.id == id_client))).scalar_one_or_none()

        return client
    
    async def find_schedule_by_id_client(self, id_client: str) -> List[Schedule]:

        return (await self.__session.execute(select(Schedule).where(Schedule.client_id == id_client))).scalars().all()
