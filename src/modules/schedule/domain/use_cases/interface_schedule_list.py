from abc import ABC, abstractmethod
from typing import Dict, List

class InterfaceScheduleListUsecase(ABC):

    @abstractmethod
    async def list(self) -> List[Dict]: pass

