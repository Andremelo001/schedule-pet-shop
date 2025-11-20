from abc import ABC, abstractmethod
from typing import Dict

class InterfaceProcessPayment(ABC):

    @abstractmethod
    async def process_notification(self, id_schedule: str, status: str) -> Dict: pass