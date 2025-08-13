from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

class InterfaceFinderPet(ABC):

    @abstractmethod
    async def finder(self, session: AsyncSession, id_pet: str) -> Dict: pass