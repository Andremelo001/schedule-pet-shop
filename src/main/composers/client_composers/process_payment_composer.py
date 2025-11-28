from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.data.use_cases.process_payment_use_case import ProcessPaymentUseCase
from src.presentation.controllers.user_controllers.process_payment_controller import ProcessPaymentController
from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.presentation.http_types.http_request import HttpRequest

async def process_payment_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository(session)
    
    use_case = ProcessPaymentUseCase(repository)

    controller = ProcessPaymentController(use_case)

    return await controller.handle(http_request)