from src.modules.schedule.domain.use_cases.interface_cancel_schedule import InterfaceCancelScheduleUsecase
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class CancelScheduleController(ControllerInterface):
    def __init__(self, use_case: InterfaceCancelScheduleUsecase):
        self.__use_case = use_case
        
    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        id_schedule = http_request.query_params["id_schedule"]

        response = await self.__use_case.cancel(id_schedule)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
