from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.pet_repository import PetRepository
from src.modules.pet.data.use_cases.pet_update_use_case import PetUpdateUseCase
from src.presentation.controllers.pet_controllers.pet_update_controller import PetUpdateController
from src.presentation.http_types.http_request import HttpRequest

async def pet_update_composer(session: AsyncSession, http_request: HttpRequest):

    repository = PetRepository(session)

    use_case = PetUpdateUseCase(repository)

    controller = PetUpdateController(use_case)

    return await controller.handle(http_request)
