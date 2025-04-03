from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.client_dto import ClientUpdateDTO

class InterfaceClientUpdate(ABC):

    @abstractmethod
    async def update(session: AsyncSession, client_id: str, client: ClientUpdateDTO) -> Dict: pass