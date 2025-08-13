from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import Dict

class InterfacePetDelete(ABC):

    @abstractmethod
    async def delete(self, session: AsyncSession, id_pet: str) -> Dict: pass