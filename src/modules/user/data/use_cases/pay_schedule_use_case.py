from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository
from src.modules.user.domain.use_cases.interface_pay_schedule import InterfacePaySchedule

from typing import Dict

import httpx

class PayScheduleUseCase(InterfacePaySchedule):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.__repository = repository
    
    async def pay_schedule(self, id_schedule: str) -> Dict:

        payments_info = await self.__payments_informations(id_schedule)

        async with httpx.AsyncClient() as client:
            payment = await client.post('http://microservice_payments:8000/payments/generate_payment', json=payments_info)

        return payment.json()

    async def __payments_informations(self, id_schedule: str) -> Dict:

        email = await self.__repository.find_email_client_by_id_schedule(id_schedule)

        schedule = await self.__repository.find_schedule_by_id(id_schedule)

        amount = schedule.total_price_schedule

        return {
            'amount': amount,
            'desc': "Pagamento via Pix",
            'email': email
        }