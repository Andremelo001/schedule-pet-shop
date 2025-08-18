from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.user.domain.use_cases.interface_client_update import InterfaceClientUpdate
from src.modules.user.dto.client_dto import ClientUpdateDTO
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class ClientUpdateController(ControllerInterface):
    def __init__(self, use_case: InterfaceClientUpdate):
        self.use_case = use_case

    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:
        
        id_client = http_request.query_params["id_client"]

        update_data = {k: v for k, v in http_request.body.items() if v is not None}

        new_client = ClientUpdateDTO(**update_data)

        response = await self.use_case.update(session, id_client, new_client)

        return HttpResponse(
            status_code=200,
             body= {
                 "message": "Informações do Cliente Atualizadas com sucesso",
                 "data": response
             }
        )