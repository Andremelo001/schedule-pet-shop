from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.pet_repository import PetRepository
from src.modules.pet.data.use_cases.pet_delete_use_case import PetDeleteUseCase
from src.presentation.controllers.pet_controllers.pet_delete_controller import PetDeleteController
from src.presentation.http_types.http_request import HttpRequest

async def pet_delete_composer(session: AsyncSession, http_request: HttpRequest):

    repository = PetRepository(session)

    use_case = PetDeleteUseCase(repository)

    controller = PetDeleteController(use_case)

    return await controller.handle(http_request)
