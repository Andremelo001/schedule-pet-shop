from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import List

from src.modules.service_types.domain.models.service import Service
from src.modules.service_types.dto.service_dto import ServiceDTO, UpdateServiceDTO

from src.modules.schedule.domain.models.schedule import Schedule

class InterfaceServiceRepository(ABC):

    @abstractmethod
    async def create_service(cls, session: AsyncSession, service: ServiceDTO) -> Service: pass

    @abstractmethod
    async def list_services(cls, session: AsyncSession) -> List[Service]: pass

    @abstractmethod
    async def find_service_by_id(cls, session: AsyncSession, id_service: str) -> Service: pass

    @abstractmethod
    async def update_service(cls, session: AsyncSession, service: UpdateServiceDTO) -> Service: pass

    @abstractmethod
    async def delete_service(cls, session: AsyncSession, id_service: str) -> None: pass

    @abstractmethod
    async def get_schedules_by_service_id(cls, session: AsyncSession, id_service: str) -> List[Schedule]: pass

    
