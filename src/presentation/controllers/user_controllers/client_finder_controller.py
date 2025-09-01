from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.user.domain.use_cases.interface_client_finder import InterfaceClientFinder
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class ClientFinderController(ControllerInterface):
    def __init__(self, use_case: InterfaceClientFinder):
        self.use_case = use_case

    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:
         
         cpf_client = http_request.query_params["cpf_client"]

         response = await self.use_case.find(session, cpf_client)

         return HttpResponse(
             status_code=200,
             body= {
                 "data": response
             }
         )
        
