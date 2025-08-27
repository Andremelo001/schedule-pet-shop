from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceScheduleListUsecase(ABC):

    @abstractmethod
    async def list(self, session: AsyncSession) -> List[Dict]: pass

