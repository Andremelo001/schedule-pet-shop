from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.pet.domain.use_cases.interface_pet_update import InterfacePetUpdate
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.pet.dto.pet_dto import PetUpdateDTO
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class PetUpdateController(ControllerInterface):
    def __init__(self, use_case: InterfacePetUpdate):
        self.use_case = use_case
    
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        id_client = http_request.query_params["id_client"]

        id_pet = http_request.query_params["id_pet"]

        update_data = {k: v for k, v in http_request.body.items() if v is not None}

        pet = PetUpdateDTO(**update_data)

        response = await self.use_case.update(session, id_client, id_pet, pet)

        return HttpResponse(
            status_code=200,
             body= {
                 "message": "Informações do Pet Atualizadas com sucesso",
                 "data": response
             }
        )