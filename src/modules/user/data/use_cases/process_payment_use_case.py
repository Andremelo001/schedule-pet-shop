from src.modules.user.domain.use_cases.interface_process_payment import InterfaceProcessPayment
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository 
from typing import Dict

class ProcessPaymentUseCase(InterfaceProcessPayment):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.__repository = repository

    async def process_notification(self, id_schedule: str, status: str) -> Dict:

        if status == "paid":
            await self.__repository.update_status_schedule(id_schedule)

        return {
            "confirmation": True,
            "message": "Notificação processada",
            "id_schedule": id_schedule,
            "status": status
        }