from abc import ABC, abstractmethod
from typing import Dict

class InterfaceGetClientWithPetsAndSchedules(ABC):

    @abstractmethod
    async def get_client_with_pets_and_schedules(self, id_client: str) -> Dict: pass