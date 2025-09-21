from abc import ABC, abstractmethod
from typing import Dict

from src.modules.user.dto.client_dto import ClientDTO

class InterfaceClientCreate(ABC):
 
    @abstractmethod
    async def create(self, client: ClientDTO) -> Dict: pass
