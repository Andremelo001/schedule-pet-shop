from typing import Dict

from src.modules.user.domain.use_cases.interface_finder_payment import InterfaceFinderPayment
from src.drivers.payment_gateway.interfaces.interface_payment_gateway import InterfacePaymentGateway

from src.errors.error_handler import HttpNotFoundError

class FinderPaymentUseCase(InterfaceFinderPayment):
    def __init__(self, payment_gateway: InterfacePaymentGateway):
        self.__payment_gateway = payment_gateway

    async def finder_payment(self, id_schedule: str) -> Dict:

        return await self.__format_response(id_schedule)

    async def __get_payment(self, id_schedule: str) -> Dict:

        payment = await self.__payment_gateway.get_payment(id_schedule)

        payment_data = payment.get("data")

        if payment_data is None:
            raise HttpNotFoundError("Pagamento não foi encontrado no banco")
        
        return payment

    async def __format_response(self, id_schedule: str) -> Dict:

        payment = await self.__get_payment(id_schedule)

        return {
            "status_payment": payment["status_payment"],
            "date_payment": payment["date_payment"]
        }