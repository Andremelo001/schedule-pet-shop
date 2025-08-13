from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.pet_repository import PetRepository
from src.modules.pet.data.use_cases.pet_finder_use_case import PetFinderUseCase
from src.presentation.controllers.pet_controllers.pet_finder_controller import PetFinderController
from src.presentation.http_types.http_request import HttpRequest

async def pet_finder_composer(session: AsyncSession, http_request: HttpRequest):

    repository = PetRepository()

    use_case = PetFinderUseCase(repository)

    controller = PetFinderController(use_case)

    return await controller.handle(session, http_request)
