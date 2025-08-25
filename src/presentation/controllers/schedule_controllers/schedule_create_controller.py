from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.schedule.domain.use_cases.interface_schedule_create import InterfaceScheduleCreateUsecase
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.modules.schedule.dto.schedule_dto import ScheduleDTO

class ScheduleCreateController(ControllerInterface):
    def __init__(self, use_case: InterfaceScheduleCreateUsecase):
        self.use_case = use_case
        
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        date_schedule = http_request.body["date_schedule"]
        time_schedule = http_request.body["time_schedule"]
        id_client = http_request.body["id_client"]
        id_pet = http_request.body["id_pet"]
        list_services = http_request.body["list_services"]

        schedule = ScheduleDTO(
            date_schedule=date_schedule,
            time_schedule=time_schedule,
            id_client=id_client,
            id_pet=id_pet,
            list_services=list_services
        )

        response = await self.use_case.create(session, schedule)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
