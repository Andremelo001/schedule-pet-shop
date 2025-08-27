from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.schedule.domain.use_cases.interface_find_schedules_actives import InterfaceFindSchedulesActivesUsecase
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindSchedulesActivesController(ControllerInterface):
    def __init__(self, use_case: InterfaceFindSchedulesActivesUsecase):
        self.use_case = use_case
        
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        response = await self.use_case.find_schedules_actives(session)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
