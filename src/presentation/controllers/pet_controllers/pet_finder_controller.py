from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.pet.domain.use_cases.interface_pet_finder import InterfaceFinderPet
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class PetFinderController(ControllerInterface):
    def __init__(self, use_case: InterfaceFinderPet):
        self.use_case = use_case
    
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        id_pet = http_request.query_params["id_pet"]

        response = await self.use_case.finder(session, id_pet)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )