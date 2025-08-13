from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user.dto.client_dto import ClientUpdateDTO

class InterfaceClientUpdate(ABC):

    @abstractmethod
    async def update(self, session: AsyncSession, client_id: str, client: ClientUpdateDTO) -> Dict: pass