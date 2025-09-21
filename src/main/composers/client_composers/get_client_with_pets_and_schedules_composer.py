from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.client_repository import ClientRepository
from src.modules.user.data.use_cases.get_client_with_pets_and_schedules_use_case import GetClientWithPetsAndSchedulesUseCase
from src.presentation.controllers.user_controllers.get_client_with_pets_and_schedules_controller import GetClientWithPetsAndSchedulesController
from src.presentation.http_types.http_request import HttpRequest

async def get_client_with_pets_and_schedules_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ClientRepository(session)

    use_case = GetClientWithPetsAndSchedulesUseCase(repository)

    controller = GetClientWithPetsAndSchedulesController(use_case)

    return await controller.handle(http_request)