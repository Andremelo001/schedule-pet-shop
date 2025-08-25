from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import List

from src.modules.service_types.domain.models.service import Service
from src.modules.service_types.dto.service_dto import ServiceDTO

class InterfaceServiceRepository(ABC):

    @abstractmethod
    async def create_service(cls, session: AsyncSession, service: ServiceDTO) -> Service: pass

    @abstractmethod
    async def list_services(cls, session: AsyncSession) -> List[Service]: pass

    
