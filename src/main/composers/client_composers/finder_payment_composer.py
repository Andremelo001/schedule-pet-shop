from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.data.use_cases.finder_payment_use_case import FinderPaymentUseCase
from src.presentation.controllers.user_controllers.finder_payment_controller import FinderPaymentController
from src.presentation.http_types.http_request import HttpRequest
from src.drivers.payment_gateway.payment_gateway_service import PaymentGatewayService

async def finder_payment_composer(session: AsyncSession, http_request: HttpRequest):
    
    payment_gateway = PaymentGatewayService()

    use_case = FinderPaymentUseCase(payment_gateway)

    controller = FinderPaymentController(use_case)

    return await controller.handle(http_request)