from abc import ABC, abstractmethod
from typing import Dict
from src.modules.service_types.dto.service_dto import ServiceDTO

class InterfaceServiceCreate(ABC):

    @abstractmethod
    async def create(self, service: ServiceDTO) -> Dict: pass