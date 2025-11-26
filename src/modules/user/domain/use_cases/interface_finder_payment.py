from abc import ABC, abstractmethod
from typing import Dict

class InterfaceFinderPayment(ABC):

    @abstractmethod
    async def finder_payment(self, id_schedule: str) -> Dict: pass