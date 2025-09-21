from abc import ABC, abstractmethod
from typing import Dict
from src.modules.service_types.dto.service_dto import UpdateServiceDTO

class InterfaceServiceUpdate(ABC):

    @abstractmethod
    async def update(self, service: UpdateServiceDTO, id_service: str) -> Dict: pass

