from src.modules.service_types.domain.use_cases.interface_service_create import InterfaceServiceCreate
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.modules.service_types.dto.service_dto import ServiceDTO

class ServiceCreateController(ControllerInterface):
    def __init__(self, use_case: InterfaceServiceCreate):
        self.__use_case = use_case
        
    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        duration_in_minutes = http_request.body["duration_in_minutes"]
        type_service = http_request.body["type_service"]
        price = http_request.body["price"]

        service = ServiceDTO(
            duration_in_minutes=duration_in_minutes,
            type_service=type_service,
            price=price,
        )

        response = await self.__use_case.create(service)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
