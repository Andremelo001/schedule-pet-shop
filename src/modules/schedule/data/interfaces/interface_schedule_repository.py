from abc import ABC, abstractmethod
from typing import List
from datetime import date
from src.modules.schedule.dto.schedule_dto import ScheduleDTO
from src.modules.schedule.domain.models.schedule import Schedule

class InterfaceScheduleRepository(ABC):

    @abstractmethod
    async def create_schedule(self, schedule: ScheduleDTO) -> None: pass

    @abstractmethod
    async def find_email_client_by_id_schedule(self, id_schedule: str) -> str: pass

    @abstractmethod
    async def find_schedule_by_id(self, id_schedule: str) -> Schedule: pass

    @abstractmethod
    async def list_schedules(self) -> List[Schedule]: pass

    @abstractmethod
    async def find_schedule_by_id_client(self, id_client: str) -> List[Schedule]: pass

    @abstractmethod
    async def cancel_schedule(self, id_schedule: str) -> None: pass

    @abstractmethod
    async def find_schedules_available(self) -> List[Schedule]: pass

    @abstractmethod
    async def delete_schedule(self, id_schedule: str) -> None: pass

    @abstractmethod
    async def duration_services_in_schedule(self, list_services: List[str]) -> int: pass

    @abstractmethod
    async def get_service_ids_from_schedule(self, schedule_id: str) -> List[str]: pass

    @abstractmethod
    async def find_schedules_by_date(self, date_schedule: date) -> List[Schedule]: pass

    @abstractmethod
    async def list_id_pets_by_client(self, id_client: str) -> List[str]: pass