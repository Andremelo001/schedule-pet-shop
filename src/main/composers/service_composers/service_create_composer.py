from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.service_repository import ServiceRepository
from src.modules.service_types.data.use_cases.service_create_use_case import ServiceCreateUseCase
from src.presentation.controllers.service_controllers.service_create_controller import ServiceCreateController
from src.presentation.http_types.http_request import HttpRequest

async def service_create_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ServiceRepository(session)

    use_case = ServiceCreateUseCase(repository)

    controller = ServiceCreateController(use_case)

    return await controller.handle(http_request)
