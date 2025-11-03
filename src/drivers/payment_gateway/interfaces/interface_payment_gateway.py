from abc import ABC, abstractmethod
from typing import Dict

class InterfacePaymentGateway(ABC):

    @abstractmethod
    async def generate_payment(self, payment_info: Dict) -> Dict: pass
