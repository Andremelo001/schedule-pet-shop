from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.user.data.use_cases.pay_schedule_use_case import PayScheduleUseCase
from src.presentation.controllers.user_controllers.pay_schedule_controller import PayScheduleController
from src.presentation.http_types.http_request import HttpRequest
from src.drivers.payment_gateway.payment_gateway_service import PaymentGatewayService

async def pay_schedule_composer(session: AsyncSession, http_request: HttpRequest):

    repository = ScheduleRepository(session)
    
    payment_gateway = PaymentGatewayService()

    use_case = PayScheduleUseCase(repository, payment_gateway)

    controller = PayScheduleController(use_case)

    return await controller.handle(http_request)