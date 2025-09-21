from abc import ABC, abstractmethod
from typing import Dict, List

class InterfaceFindSchedulesActivesUsecase(ABC):

    @abstractmethod
    async def find_schedules_actives(self) -> List[Dict]: pass

