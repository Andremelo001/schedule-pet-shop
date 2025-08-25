from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.schedule.dto.schedule_dto import ScheduleDTO, ScheduleUpdateDTO
from src.modules.schedule.domain.models.schedule import Schedule

class InterfaceScheduleRepository(ABC):

    @abstractmethod
    async def create_schedule(cls, session: AsyncSession, schedule: ScheduleDTO) -> None: pass

    @abstractmethod
    async def list_schedules(cls, session: AsyncSession) -> List[Schedule]: pass

    @abstractmethod
    async def find_schedule_by_id_client(cls, session: AsyncSession, id_client: str) -> List[Schedule]: pass

    @abstractmethod
    async def cancel_schedule(cls, session: AsyncSession, id_schedule: str) -> None: pass

    @abstractmethod
    async def find_schedules_available(cls, session: AsyncSession) -> List[Schedule]: pass

    @abstractmethod
    async def delete_schedule(cls, session: AsyncSession, id_schedule: str) -> None: pass

    @abstractmethod
    async def update_schedule(cls, session: AsyncSession, id_schedule: str, schedule: ScheduleUpdateDTO) -> Schedule: pass

    @abstractmethod
    async def duration_services_in_schedule(cls, session: AsyncSession, list_services: List[str]) -> int: pass

    @abstractmethod
    async def get_service_ids_from_schedule(cls, session: AsyncSession, schedule_id: str) -> List[str]: pass

    @abstractmethod
    async def find_schedules_by_date(cls, session: AsyncSession, date_schedule: date) -> List[Schedule]: pass