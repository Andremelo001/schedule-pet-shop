from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.service_repository import ServiceRepository
from src.modules.service_types.data.use_cases.service_update_use_case import ServiceUpdateUseCase
from src.presentation.controllers.service_controllers.service_update_controller import ServiceUpdateController
from src.presentation.http_types.http_request import HttpRequest

async def service_update_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ServiceRepository(session)

    use_case = ServiceUpdateUseCase(repository)

    controller = ServiceUpdateController(use_case)

    return await controller.handle(http_request)