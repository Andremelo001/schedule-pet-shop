from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.schedule.domain.use_cases.interface_schedule_list import InterfaceScheduleListUsecase
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository

from src.modules.schedule.domain.models.schedule import Schedule

class ScheduleListUseCase(InterfaceScheduleListUsecase):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.repository = repository

    async def list(self, session: AsyncSession) -> List[Dict]:

        schedules = await self.repository.list_schedules(session)

        return self.__format_response(schedules)

    def __format_response(cls, schedules: List[Schedule]) -> List[Dict]:

        return [
            {
                "id": str(schedule.id),
                "date_schedule": str(schedule.date_schedule),
                "time_schedule": str(schedule.time_schedule),
                "client_id": str(schedule.client_id),
                "pet_id": str(schedule.pet_id),
                "total_price_schedule": schedule.total_price_schedule,
                "schedule_active": schedule.schedule_active,
                "services": [str(service.id) for service in schedule.services]
            }
            for schedule in schedules
        ]