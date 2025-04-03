from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

from src.domain.models.client import Client
from src.dto.client_dto import ClientDTO, ClientUpdateDTO

class InterfaceClientRepository(ABC):

    @abstractmethod
    async def get_client(self, session: AsyncSession, cpf_client: str) -> Client: pass

    @abstractmethod
    async def create_client(self, session: AsyncSession, client: ClientDTO) -> Client: pass

    @abstractmethod
    async def update_client(self, session: AsyncSession, id_client: str, client: ClientUpdateDTO) -> Client: pass

    @abstractmethod
    async def delete_client(cls, session: AsyncSession, id_client: str) -> None: pass

        



