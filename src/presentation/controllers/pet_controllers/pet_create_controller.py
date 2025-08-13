from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.pet.domain.use_cases.interface_pet_create import InterfacePetCreate
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.modules.pet.dto.pet_dto import PetDTO

class PetCreateController(ControllerInterface):
    def __init__(self, use_case: InterfacePetCreate):
        self.use_case = use_case
    
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        id_client = http_request.body["id_client"]
        name = http_request.body["name"]
        breed = http_request.body["breed"]
        age = http_request.body["age"]
        size_in_centimeters = http_request.body["size_in_centimeters"]

        pet = PetDTO(
            id_client=id_client,
            name=name,
            breed=breed,
            age=age,
            size_in_centimeters=size_in_centimeters
        )

        response = await self.use_case.create(session, pet, id_client)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )