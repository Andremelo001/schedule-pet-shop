from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.schedule.data.use_cases.schedule_delete_use_case import ScheduleDeleteUseCase
from src.presentation.controllers.schedule_controllers.schedule_delete_controller import ScheduleDeleteController
from src.presentation.http_types.http_request import HttpRequest

async def schedule_delete_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository(session)

    use_case = ScheduleDeleteUseCase(repository)

    controller = ScheduleDeleteController(use_case)

    return await controller.handle(http_request)
