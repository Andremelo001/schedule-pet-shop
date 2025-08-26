from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceRequestCancelScheduleUsecase(ABC):

    @abstractmethod
    async def request_cancel(self, session: AsyncSession, id_schedule: str) -> Dict: pass