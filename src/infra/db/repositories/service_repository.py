from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from typing import List

from sqlmodel import select

from src.modules.service_types.data.interfaces.interface_service_repository import InterfaceServiceRepository
from src.modules.service_types.domain.models.service import Service
from src.infra.db.entities.services import Services as ServicesEntitie
from src.modules.service_types.dto.service_dto import ServiceDTO

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
    async def list_services(cls, session: AsyncSession) -> List[Service]:

        return (await session.execute(select(ServicesEntitie))).scalars().all()
