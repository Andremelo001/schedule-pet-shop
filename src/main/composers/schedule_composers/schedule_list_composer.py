from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.schedule.data.use_cases.schedule_list_use_case import ScheduleListUseCase
from src.presentation.controllers.schedule_controllers.schedule_list_controller import ScheduleListController
from src.presentation.http_types.http_request import HttpRequest

async def schedule_list_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository()

    use_case = ScheduleListUseCase(repository)

    controller = ScheduleListController(use_case)

    return await controller.handle(session, http_request)
