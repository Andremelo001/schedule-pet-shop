from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceScheduleDeleteUsecase(ABC):

    @abstractmethod
    async def delete(self, session: AsyncSession, id_schedule: str) -> Dict: pass
