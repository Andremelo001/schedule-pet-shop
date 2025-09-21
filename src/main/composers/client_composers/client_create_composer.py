from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.client_repository import ClientRepository
from src.modules.user.data.use_cases.client_create_use_case import CreateClientUseCase
from src.presentation.controllers.user_controllers.client_create_controller import ClientCreateController
from src.presentation.http_types.http_request import HttpRequest

async def client_create_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ClientRepository(session)

    use_case = CreateClientUseCase(repository)

    controller = ClientCreateController(use_case)

    return await controller.handle(http_request)
