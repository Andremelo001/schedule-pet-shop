from src.presentation.http_types.http_request import HttpRequest
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.repositories.client_repository import ClientRepository
from src.data.use_cases.client_delete_use_case import ClientDeleteUseCase
from src.presentation.controllers.client_delete_controller import ClientDeleteController

async def client_delete_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ClientRepository()

    use_case = ClientDeleteUseCase(repository)

    controller = ClientDeleteController(use_case)

    return await controller.handle(session, http_request)