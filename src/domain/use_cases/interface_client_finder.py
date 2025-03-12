from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.client import Client

class InterfaceClientFinder(ABC):

    @abstractmethod
    async def find(self, session: AsyncSession, cpf_client: str) -> Client: pass
