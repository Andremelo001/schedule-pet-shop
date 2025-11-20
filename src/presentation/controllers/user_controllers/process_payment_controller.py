from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.user.domain.use_cases.interface_process_payment import InterfaceProcessPayment

class ProcessPaymentController(ControllerInterface):
    def __init__(self, use_case: InterfaceProcessPayment):
        self.__use_case = use_case

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        
        status = http_request.body.get("status")
        schedule_id = http_request.body.get("schedule_id")

        response = await self.__use_case.process_notification(schedule_id, status)

        return HttpResponse(
            status_code=200,
            body=response
        )