from src.modules.user.domain.use_cases.interface_process_payment import InterfaceProcessPayment
from typing import Dict

class ProcessPaymentUseCase(InterfaceProcessPayment):

    async def process_notification(self, id_schedule: str, status: str) -> Dict:

        return {
            "confirmation": True,
            "message": "Pagamento Confirmado com sucesso",
            "id_schedule": id_schedule,
            "status": status
        }