from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.schedule.data.use_cases.cancel_schedule_use_case import CancelScheduleUseCase
from src.presentation.controllers.schedule_controllers.cancel_schedule_controller import CancelScheduleController
from src.presentation.http_types.http_request import HttpRequest

async def cancel_schedule(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository(session)

    use_case = CancelScheduleUseCase(repository)

    controller = CancelScheduleController(use_case)

    return await controller.handle(http_request)
