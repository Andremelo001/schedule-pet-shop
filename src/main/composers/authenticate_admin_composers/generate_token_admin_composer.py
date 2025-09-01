from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.admin_repository import AdminRepository
from src.presentation.controllers.authenticated_admin_controller.generate_token_admin_controller import GenerateTokenAdminController
from src.modules.authenticate_admin.data.use_cases.authenticate_admin_use_case import AutheticateAdminUseCase
from src.presentation.http_types.http_request import HttpRequest

async def generate_token_admin_composer(session: AsyncSession, http_request: HttpRequest):

    repository = AdminRepository()

    use_case = AutheticateAdminUseCase(repository)

    controller = GenerateTokenAdminController(use_case)

    return await controller.handle(session, http_request)

