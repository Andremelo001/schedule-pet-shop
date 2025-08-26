from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.service_types.domain.use_cases.interface_service_delete import InterfaceServiceDelete
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.modules.service_types.dto.service_dto import ServiceDTO

class ServiceDeleteController(ControllerInterface):
    def __init__(self, use_case: InterfaceServiceDelete):
        self.use_case = use_case
        
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        id_service = http_request.query_params["id_service"]

        response = await self.use_case.delete(session, id_service)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
