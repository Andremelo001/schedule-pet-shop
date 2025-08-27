from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from typing import List

from sqlmodel import select

from src.modules.service_types.data.interfaces.interface_service_repository import InterfaceServiceRepository
from src.modules.service_types.domain.models.service import Service
from src.infra.db.entities.services import Services as ServicesEntitie
from src.modules.service_types.dto.service_dto import ServiceDTO, UpdateServiceDTO

from src.infra.db.entities.schedule import ScheduleServices, Schedule as ScheduleEntitie
from src.modules.schedule.domain.models.schedule import Schedule

class ServiceRepository(InterfaceServiceRepository):

    @classmethod
    async def create_service(cls, session: AsyncSession, service: ServiceDTO) -> Service:
        try:
            new_service = ServicesEntitie(
                id= uuid4(),
                duration_in_minutes=service.duration_in_minutes,
                type_service=service.type_service,
                price=service.price
            )

            session.add(new_service)
            await session.commit()
            await session.refresh(new_service)

        except Exception as exception:
            await session.rollback()
            raise exception
        
    @classmethod
    async def find_service_by_id(cls, session: AsyncSession, id_service: str) -> Service:

        service = (await session.execute(select(ServicesEntitie).where(ServicesEntitie.id == id_service))).scalar_one_or_none()

        return service
    
    @classmethod
    async def list_services(cls, session: AsyncSession) -> List[Service]:

        return (await session.execute(select(ServicesEntitie))).scalars().all()
    
    async def update_service(cls, session: AsyncSession, service: UpdateServiceDTO, id_service: str) -> Service:

        new_service = (await session.execute(select(ServicesEntitie).where(ServicesEntitie.id == id_service))).scalar_one_or_none()

        for key, value in service.model_dump(exclude_unset=True).items():
            setattr(new_service, key, value)

        await session.commit()
        await session.refresh(new_service)

        return new_service

    async def delete_service(cls, session: AsyncSession, id_service: str) -> None:

        service = (await session.execute(select(ServicesEntitie).where(ServicesEntitie.id == id_service))).scalar_one_or_none()

        await session.delete(service)

        await session.commit()

    async def get_schedules_by_service_id(cls, session: AsyncSession, id_service: str) -> List[Schedule]:

        schedules = await session.execute(select(ScheduleEntitie).join(ScheduleServices, ScheduleEntitie.id == ScheduleServices.schedule_id).where(ScheduleServices.services_id == id_service))

        return schedules.scalars().all()