from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.schedule.data.use_cases.schedule_create_use_case import ScheduleCreateUseCase
from src.presentation.controllers.schedule_controllers.schedule_create_controller import ScheduleCreateController
from src.presentation.http_types.http_request import HttpRequest

async def schedule_create_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository(session)

    use_case = ScheduleCreateUseCase(repository)

    controller = ScheduleCreateController(use_case)

    return await controller.handle(http_request)
