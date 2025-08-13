from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.pet.domain.use_cases.interface_get_all_pets_by_cpf_client import InterfaceGetAllPetsByCpfClient
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetAllPetsController(ControllerInterface):
    def __init__(self, use_case: InterfaceGetAllPetsByCpfClient):
        self.use_case = use_case
    
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        cpf_client = http_request.query_params["cpf_client"]

        response = await self.use_case.get_all_pets(session, cpf_client)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )