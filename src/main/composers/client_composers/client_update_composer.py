from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.client_repository import ClientRepository
from src.modules.user.data.use_cases.client_update_use_case import ClientUpdateUseCase
from src.presentation.controllers.user_controllers.client_update_controller import ClientUpdateController
from src.presentation.http_types.http_request import HttpRequest

async def client_update_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ClientRepository(session)

    use_case = ClientUpdateUseCase(repository)

    controller = ClientUpdateController(use_case)

    return await controller.handle(http_request)