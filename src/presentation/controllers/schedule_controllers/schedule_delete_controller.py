from src.modules.schedule.domain.use_cases.interface_schedule_delete import InterfaceScheduleDeleteUsecase
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class ScheduleDeleteController(ControllerInterface):
    def __init__(self, use_case: InterfaceScheduleDeleteUsecase):
        self.__use_case = use_case
        
    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        id_schedule = http_request.query_params["id_schedule"]

        response = await self.__use_case.delete(id_schedule)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
