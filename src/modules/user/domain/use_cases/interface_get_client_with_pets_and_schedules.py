from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceGetClientWithPetsAndSchedules(ABC):

    @abstractmethod
    async def get_client_with_pets_and_schedules(self, session: AsyncSession, id_client: str) -> Dict: pass