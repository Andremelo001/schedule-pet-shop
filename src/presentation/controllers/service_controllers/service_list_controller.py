from src.modules.service_types.domain.use_cases.interface_service_list import InterfaceServiceList
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class ServiceListController(ControllerInterface):
    def __init__(self, use_case: InterfaceServiceList):
        self.__use_case = use_case
        
    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        response = await self.__use_case.list()

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
