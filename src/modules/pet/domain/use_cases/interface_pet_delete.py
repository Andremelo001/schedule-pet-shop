from abc import ABC, abstractmethod
from typing import Dict

class InterfacePetDelete(ABC):

    @abstractmethod
    async def delete(self, id_pet: str) -> Dict: pass