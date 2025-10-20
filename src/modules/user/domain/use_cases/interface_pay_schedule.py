from abc import ABC, abstractmethod
from typing import Dict

class InterfacePaySchedule(ABC):

    @abstractmethod
    async def pay_schedule(self, id_schedule: str) -> Dict: pass