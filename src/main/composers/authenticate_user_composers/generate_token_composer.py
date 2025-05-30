from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.client_repository import ClientRepository
from src.presentation.controllers.authenticated_user_controllers.generate_token_controller import GenerateTokenController
from src.modules.authenticate_user.data.use_case.authenticate_user_use_case import AuthenticateUserUseCase
from src.presentation.http_types.http_request import HttpRequest

async def generate_token_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ClientRepository()

    use_case = AuthenticateUserUseCase(repository)

    controller = GenerateTokenController(use_case)

    return await controller.handle(session, http_request)

