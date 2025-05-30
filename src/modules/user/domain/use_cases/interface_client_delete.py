from abc import ABC, abstractmethod
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceClientDelete(ABC):

    @abstractmethod
    async def delete(self, session: AsyncSession, id_client: str) -> Dict: pass