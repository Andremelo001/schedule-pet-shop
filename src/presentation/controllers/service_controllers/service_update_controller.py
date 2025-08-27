from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.service_types.domain.use_cases.interface_service_update import InterfaceServiceUpdate
from src.modules.service_types.dto.service_dto import UpdateServiceDTO
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class ServiceUpdateController(ControllerInterface):
    def __init__(self, use_case: InterfaceServiceUpdate):
        self.use_case = use_case

    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:
        
        id_service = http_request.query_params["id_service"]

        update_data = {k: v for k, v in http_request.body.items() if v is not None}

        new_service = UpdateServiceDTO(**update_data)

        response = await self.use_case.update(session, new_service, id_service)

        return HttpResponse(
            status_code=200,
             body= {
                 "message": "Informações do Serviço Atualizadas com sucesso",
                 "data": response
             }
        )