from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

from src.domain.models.client import Client
from src.dto.client_dto import ClientDTO

class InterfaceClientRepository(ABC):

    @abstractmethod
    async def get_client(self, session: AsyncSession, cpf_client: str) -> Client: pass

    @abstractmethod
    async def create_client(self, session: AsyncSession, client: ClientDTO) -> Client: pass

        



