from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.service_repository import ServiceRepository
from src.modules.service_types.data.use_cases.service_delete_use_case import ServiceDeleteUseCase
from src.presentation.controllers.service_controllers.service_delete_controller import ServiceDeleteController
from src.presentation.http_types.http_request import HttpRequest

async def service_delete_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ServiceRepository(session)

    use_case = ServiceDeleteUseCase(repository)

    controller = ServiceDeleteController(use_case)

    return await controller.handle(http_request)
