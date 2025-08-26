from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.schedule.data.use_cases.request_cancel_schedule_use_case import RequestCancelScheduleUseCase
from src.presentation.controllers.schedule_controllers.request_cancel_schedule_controller import RequestCancelScheduleController
from src.presentation.http_types.http_request import HttpRequest

async def request_cancel_schedule(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository()

    use_case = RequestCancelScheduleUseCase(repository)

    controller = RequestCancelScheduleController(use_case)

    return await controller.handle(session, http_request)
