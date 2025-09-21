from abc import ABC, abstractmethod
from typing import Dict

class InterfaceClientFinder(ABC):

    @abstractmethod
    async def find(self, cpf_client: str) -> Dict: pass
