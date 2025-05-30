from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.client_repository import ClientRepository
from src.modules.user.data.use_cases.client_finder_use_case import ClientFinderUseCase
from src.presentation.controllers.user_controllers.client_finder_controller import ClientFinderController
from src.presentation.http_types.http_request import HttpRequest

async def client_finder_composer(session: AsyncSession, http_request: HttpRequest):
    
    repository = ClientRepository()

    use_case = ClientFinderUseCase(repository)

    controller = ClientFinderController(use_case)

    return await controller.handle(session, http_request)

