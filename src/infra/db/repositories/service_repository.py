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
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_service(self, service: ServiceDTO) -> Service:
        try:
            new_service = ServicesEntitie(
                id= uuid4(),
                duration_in_minutes=service.duration_in_minutes,
                type_service=service.type_service,
                price=service.price
            )

            self.__session.add(new_service)
            await self.__session.commit()
            await self.__session.refresh(new_service)

        except Exception as exception:
            await self.__session.rollback()
            raise exception
        
    async def find_service_by_id(self, id_service: str) -> Service:

        service = (await self.__session.execute(select(ServicesEntitie).where(ServicesEntitie.id == id_service))).scalar_one_or_none()

        return service
    
    async def list_services(self) -> List[Service]:

        return (await self.__session.execute(select(ServicesEntitie))).scalars().all()
    
    async def update_service(self, service: UpdateServiceDTO, id_service: str) -> Service:

        new_service = (await self.__session.execute(select(ServicesEntitie).where(ServicesEntitie.id == id_service))).scalar_one_or_none()

        for key, value in service.model_dump(exclude_unset=True).items():
            setattr(new_service, key, value)

        await self.__session.commit()
        await self.__session.refresh(new_service)

        return new_service

    async def delete_service(self, id_service: str) -> None:

        service = (await self.__session.execute(select(ServicesEntitie).where(ServicesEntitie.id == id_service))).scalar_one_or_none()

        await self.__session.delete(service)

        await self.__session.commit()

    async def get_schedules_by_service_id(self, id_service: str) -> List[Schedule]:

        schedules = await self.__session.execute(select(ScheduleEntitie).join(ScheduleServices, ScheduleEntitie.id == ScheduleServices.schedule_id).where(ScheduleServices.services_id == id_service))

        return schedules.scalars().all()