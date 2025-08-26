from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.schedule.domain.use_cases.interface_cancel_schedule import InterfaceCancelScheduleUsecase
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class CancelScheduleController(ControllerInterface):
    def __init__(self, use_case: InterfaceCancelScheduleUsecase):
        self.use_case = use_case
        
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        id_schedule = http_request.query_params["id_schedule"]

        response = await self.use_case.cancel(session, id_schedule)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
