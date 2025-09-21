from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.user.domain.use_cases.interface_get_client_with_pets_and_schedules import InterfaceGetClientWithPetsAndSchedules
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetClientWithPetsAndSchedulesController(ControllerInterface):
    def __init__(self, use_case: InterfaceGetClientWithPetsAndSchedules):
        self.__use_case = use_case

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        
        id_client = http_request.query_params["id_client"]

        response = await self.__use_case.get_client_with_pets_and_schedules(id_client)

        return HttpResponse(
            status_code=200,
             body= {
                 "data": response
             }
        )