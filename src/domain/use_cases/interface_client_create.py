from abc import ABC, abstractmethod
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.client_dto import ClientDTO

class InterfaceClientCreate(ABC):
 
    @abstractmethod
    async def create(self, session: AsyncSession, client: ClientDTO) -> Dict: pass
