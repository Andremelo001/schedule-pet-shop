from abc import ABC, abstractmethod
from typing import Dict

class InterfaceCancelScheduleUsecase(ABC):

    @abstractmethod
    async def cancel(self, id_schedule: str) -> Dict: pass