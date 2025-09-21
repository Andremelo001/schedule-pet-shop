from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.pet_repository import PetRepository
from src.modules.pet.data.use_cases.get_all_pets_by_cpf_client_use_case import GetAllPetsByCpfClientUseCase
from src.presentation.controllers.pet_controllers.get_all_pets_controller import GetAllPetsController
from src.presentation.http_types.http_request import HttpRequest

async def get_all_pets_composer(session: AsyncSession, http_request: HttpRequest):

    repository = PetRepository(session)

    use_case = GetAllPetsByCpfClientUseCase(repository)

    controller = GetAllPetsController(use_case)

    return await controller.handle(http_request)
