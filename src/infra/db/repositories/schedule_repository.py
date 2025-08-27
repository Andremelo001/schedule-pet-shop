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

from src.infra.db.entities.client import Client

class ScheduleRepository(InterfaceScheduleRepository):

    @classmethod
    async def create_schedule(cls, session: AsyncSession, schedule: ScheduleDTO) -> None:

        price_total = 0

        for id_service in schedule.list_services:

           service = (await session.execute(select(Services).where(Services.id == id_service))).scalar_one_or_none()

           price_total += service.price

        try:

            new_schedule = ScheduleEntitie(
                id = uuid4(),
                date_schedule= schedule.date_schedule,
                time_schedule= schedule.time_schedule,
                total_price_schedule= price_total,
                schedule_active= True,
                client_id= schedule.id_client,
                pet_id= schedule.id_pet
            )

            session.add(new_schedule)
            await session.commit()
            await session.refresh(new_schedule)

            for id_service in schedule.list_services:

                association = ScheduleServices(schedule_id=new_schedule.id, services_id=id_service)

                session.add(association)
            
            await session.commit()

        except Exception as exception:
            await session.rollback()
            raise exception
        
    @classmethod
    async def find_email_client_by_id_schedule(cls, session: AsyncSession, id_schedule: str) -> str:

        result = await session.execute(select(Client.email).join(ScheduleEntitie, ScheduleEntitie.client_id == Client.id).where(ScheduleEntitie.id == id_schedule))
        
        return result.scalar_one_or_none()
        
    @classmethod
    async def find_schedule_by_id(cls, session: AsyncSession, id_schedule: str) -> Schedule:

        schedule = (await session.execute(select(ScheduleEntitie).where(ScheduleEntitie.id == id_schedule))).scalar_one_or_none()

        return schedule
    
    @classmethod
    async def list_schedules(cls, session: AsyncSession) -> List[Schedule]:

        return (await session.execute(select(ScheduleEntitie).options(selectinload(ScheduleEntitie.services)))).scalars().all()

    @classmethod
    async def find_schedule_by_id_client(cls, session: AsyncSession, id_client: str) -> List[Schedule]:

        return (await session.execute(select(ScheduleEntitie).where(ScheduleEntitie.client_id == id_client))).scalars().all()

    @classmethod
    async def cancel_schedule(cls, session: AsyncSession, id_schedule: str) -> None:

        schedule = (await session.execute(select(ScheduleEntitie).where(ScheduleEntitie.id == id_schedule))).scalar_one_or_none()

        schedule.schedule_active = False

        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)

    @classmethod
    async def find_schedules_available(cls, session: AsyncSession) -> List[Schedule]:

        return (await session.execute(select(ScheduleEntitie).options(selectinload(ScheduleEntitie.services)).where(ScheduleEntitie.schedule_active == True))).scalars().all()

    @classmethod
    async def delete_schedule(cls, session: AsyncSession, id_schedule: str) -> None:

        schedule = (await session.execute(select(ScheduleEntitie).where(ScheduleEntitie.id == id_schedule))).scalar_one_or_none()

        await session.delete(schedule)
        await session.commit()
    
    @classmethod
    async def duration_services_in_schedule(cls, session: AsyncSession, list_services: List[str]) -> int:

        temp_total = 0

        for id_service in list_services:

           service = (await session.execute(select(Services).where(Services.id == id_service))).scalar_one_or_none()

           temp_total += service.duration_in_minutes
        
        return temp_total

    @classmethod
    async def get_service_ids_from_schedule(cls, session: AsyncSession, schedule_id: str) -> List[str]:
        
        result = await session.execute(
            select(ScheduleServices.services_id)
            .where(ScheduleServices.schedule_id == schedule_id)
        )
        
        service_ids = result.scalars().all()
        return [str(service_id) for service_id in service_ids]

    @classmethod
    async def find_schedules_by_date(cls, session: AsyncSession, date_schedule: date) -> List[Schedule]:
        
        return (await session.execute(
            select(ScheduleEntitie)
            .where(ScheduleEntitie.date_schedule == date_schedule)
            .where(ScheduleEntitie.schedule_active == True)
        )).scalars().all()
