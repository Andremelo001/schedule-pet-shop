from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.user.domain.use_cases.interface_pay_schedule import InterfacePaySchedule
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class PayScheduleController(ControllerInterface):
    def __init__(self, use_case: InterfacePaySchedule):
        self.__use_case = use_case

    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        id_schedule = http_request.query_params["id_schedule"]

        response = await self.__use_case.pay_schedule(id_schedule)

        return HttpResponse(
            status_code=200,
             body= {
                "message": "Realize o pagamento do Agendamento!",
                "data": response
             }
        )