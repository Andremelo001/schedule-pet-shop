from abc import ABC, abstractmethod
from typing import Dict

class InterfaceScheduleDeleteUsecase(ABC):

    @abstractmethod
    async def delete(self, id_schedule: str) -> Dict: pass
