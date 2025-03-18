from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

class InterfaceClientFinder(ABC):

    @abstractmethod
    async def find(self, session: AsyncSession, cpf_client: str) -> Dict: pass
