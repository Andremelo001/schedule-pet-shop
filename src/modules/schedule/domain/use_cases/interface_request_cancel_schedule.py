from abc import ABC, abstractmethod
from typing import Dict

class InterfaceRequestCancelScheduleUsecase(ABC):

    @abstractmethod
    async def request_cancel(self, id_schedule: str) -> Dict: pass