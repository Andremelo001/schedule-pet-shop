from abc import ABC, abstractmethod
from typing import Dict

class InterfaceClientDelete(ABC):

    @abstractmethod
    async def delete(self, id_client: str) -> Dict: pass