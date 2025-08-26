from abc import ABC, abstractmethod
from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceServiceList(ABC):

    @abstractmethod
    async def list(self, session: AsyncSession) -> List[Dict]: pass