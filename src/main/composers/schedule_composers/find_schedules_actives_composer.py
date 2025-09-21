from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.schedule.data.use_cases.find_schedules_actives import FindSchedulesActivesUseCase
from src.presentation.controllers.schedule_controllers.find_schedules_actives_controller import FindSchedulesActivesController
from src.presentation.http_types.http_request import HttpRequest

async def find_schedules_actives_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository(session)

    use_case = FindSchedulesActivesUseCase(repository)

    controller = FindSchedulesActivesController(use_case)

    return await controller.handle(http_request)
