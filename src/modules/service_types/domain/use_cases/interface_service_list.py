from abc import ABC, abstractmethod
from typing import List, Dict

class InterfaceServiceList(ABC):

    @abstractmethod
    async def list(self) -> List[Dict]: pass