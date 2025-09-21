from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.pet_repository import PetRepository
from src.modules.pet.data.use_cases.pet_create_use_case import PetCreateUseCase
from src.presentation.controllers.pet_controllers.pet_create_controller import PetCreateController
from src.presentation.http_types.http_request import HttpRequest

async def pet_create_composer(session: AsyncSession, http_request: HttpRequest):

    repository = PetRepository(session)

    use_case = PetCreateUseCase(repository)

    controller = PetCreateController(use_case)

    return await controller.handle(http_request)
