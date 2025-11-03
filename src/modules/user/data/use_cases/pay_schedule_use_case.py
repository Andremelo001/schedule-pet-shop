from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository
from src.modules.user.domain.use_cases.interface_pay_schedule import InterfacePaySchedule
from src.drivers.payment_gateway.interfaces.interface_payment_gateway import InterfacePaymentGateway

from typing import Dict
class PayScheduleUseCase(InterfacePaySchedule):
    def __init__(
        self, 
        repository: InterfaceScheduleRepository,
        payment_gateway: InterfacePaymentGateway
    ):
        self.__repository = repository
        self.__payment_gateway = payment_gateway
    
    async def pay_schedule(self, id_schedule: str) -> Dict:

        payments_info = await self.__payments_informations(id_schedule)

        payment = await self.__payment_gateway.generate_payment(payments_info)
        
        return payment

    async def __payments_informations(self, id_schedule: str) -> Dict:

        email = await self.__repository.find_email_client_by_id_schedule(id_schedule)

        schedule = await self.__repository.find_schedule_by_id(id_schedule)

        amount = schedule.total_price_schedule

        return {
            'amount': amount,
            'desc': "Pagamento via Pix",
            'email': email
        }