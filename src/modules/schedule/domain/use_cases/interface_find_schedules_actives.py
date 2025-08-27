from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceFindSchedulesActivesUsecase(ABC):

    @abstractmethod
    async def find_schedules_actives(self, session: AsyncSession) -> List[Dict]: pass

