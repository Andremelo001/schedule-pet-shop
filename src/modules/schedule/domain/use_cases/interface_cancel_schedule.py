from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceCancelScheduleUsecase(ABC):

    @abstractmethod
    async def cancel(self, session: AsyncSession, id_schedule: str) -> Dict: pass