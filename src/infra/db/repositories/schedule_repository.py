from typing import List
from uuid import uuid4
from datetime import date
from sqlmodel import select
from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.schedule.dto.schedule_dto import ScheduleDTO
from src.modules.schedule.domain.models.schedule import Schedule
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository
from src.infra.db.entities.services import Services
from src.infra.db.entities.schedule import Schedule as ScheduleEntitie, ScheduleServices
from src.infra.db.entities.pet import Pet
from src.infra.db.entities.client import Client

class ScheduleRepository(InterfaceScheduleRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_schedule(self, schedule: ScheduleDTO) -> None:

        price_total = 0

        for id_service in schedule.list_services:

           service = (await self.__session.execute(select(Services).where(Services.id == id_service))).scalar_one_or_none()

           price_total += service.price

        try:

            new_schedule = ScheduleEntitie(
                id = uuid4(),
                date_schedule= schedule.date_schedule,
                time_schedule= schedule.time_schedule,
                total_price_schedule= price_total,
                schedule_active= False,
                client_id= schedule.id_client,
                pet_id= schedule.id_pet
            )

            self.__session.add(new_schedule)
            await self.__session.commit()
            await self.__session.refresh(new_schedule)

            for id_service in schedule.list_services:

                association = ScheduleServices(schedule_id=new_schedule.id, services_id=id_service)

                self.__session.add(association)
            
            await self.__session.commit()

        except Exception as exception:
            await self.__session.rollback()
            raise exception
        
    async def find_email_client_by_id_schedule(self, id_schedule: str) -> str:

        result = await self.__session.execute(select(Client.email).join(ScheduleEntitie, ScheduleEntitie.client_id == Client.id).where(ScheduleEntitie.id == id_schedule))
        
        return result.scalar_one_or_none()
        
    async def find_schedule_by_id(self, id_schedule: str) -> Schedule:

        schedule = (await self.__session.execute(select(ScheduleEntitie).where(ScheduleEntitie.id == id_schedule))).scalar_one_or_none()

        return schedule
    
    async def list_schedules(self) -> List[Schedule]:

        return (await self.__session.execute(select(ScheduleEntitie).options(selectinload(ScheduleEntitie.services)))).scalars().all()

    async def find_schedule_by_id_client(self, id_client: str) -> List[Schedule]:

        return (await self.__session.execute(select(ScheduleEntitie).where(ScheduleEntitie.client_id == id_client))).scalars().all()

    async def cancel_schedule(self, id_schedule: str) -> None:

        schedule = (await self.__session.execute(select(ScheduleEntitie).where(ScheduleEntitie.id == id_schedule))).scalar_one_or_none()

        schedule.schedule_active = False

        self.__session.add(schedule)
        await self.__session.commit()
        await self.__session.refresh(schedule)

    async def find_schedules_available(self) -> List[Schedule]:

        return (await self.__session.execute(select(ScheduleEntitie).options(selectinload(ScheduleEntitie.services)).where(ScheduleEntitie.schedule_active == True))).scalars().all()

    async def delete_schedule(self, id_schedule: str) -> None:

        schedule = (await self.__session.execute(select(ScheduleEntitie).where(ScheduleEntitie.id == id_schedule))).scalar_one_or_none()

        await self.__session.delete(schedule)
        await self.__session.commit()
    
    async def duration_services_in_schedule(self, list_services: List[str]) -> int:

        temp_total = 0

        for id_service in list_services:

           service = (await self.__session.execute(select(Services).where(Services.id == id_service))).scalar_one_or_none()

           temp_total += service.duration_in_minutes
        
        return temp_total

    async def get_service_ids_from_schedule(self, schedule_id: str) -> List[str]:
        
        result = await self.__session.execute(
            select(ScheduleServices.services_id)
            .where(ScheduleServices.schedule_id == schedule_id)
        )
        
        service_ids = result.scalars().all()
        return [str(service_id) for service_id in service_ids]

    async def find_schedules_by_date(self, date_schedule: date) -> List[Schedule]:
        
        return (await self.__session.execute(
            select(ScheduleEntitie)
            .where(ScheduleEntitie.date_schedule == date_schedule)
            .where(ScheduleEntitie.schedule_active == True)
        )).scalars().all()
    
    async def list_id_pets_by_client(self, id_client: str) -> List[str]:
        
        pets = (await self.__session.execute(select(Pet).where(Pet.client_id == id_client))).scalars().all()

        return [str(pet.id) for pet in pets]
    
    async def update_status_schedule(self, id_schedule: str) -> None:

        schedule = (await self.__session.execute(select(ScheduleEntitie).where(ScheduleEntitie.id == id_schedule))).scalar_one_or_none()

        schedule.schedule_active = True

        await self.__session.commit()