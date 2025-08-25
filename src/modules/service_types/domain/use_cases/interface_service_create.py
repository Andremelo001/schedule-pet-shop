from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.service_types.dto.service_dto import ServiceDTO

class InterfaceServiceCreate(ABC):

    @abstractmethod
    async def create(self, session: AsyncSession, service: ServiceDTO) -> Dict: pass