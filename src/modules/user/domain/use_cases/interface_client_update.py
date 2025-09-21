from abc import ABC, abstractmethod
from typing import Dict

from src.modules.user.dto.client_dto import ClientUpdateDTO

class InterfaceClientUpdate(ABC):

    @abstractmethod
    async def update(self, client_id: str, client: ClientUpdateDTO) -> Dict: pass