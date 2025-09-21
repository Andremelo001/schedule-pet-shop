from abc import ABC, abstractmethod
from typing import Dict

class InterfaceFinderPet(ABC):

    @abstractmethod
    async def finder(self, id_pet: str) -> Dict: pass