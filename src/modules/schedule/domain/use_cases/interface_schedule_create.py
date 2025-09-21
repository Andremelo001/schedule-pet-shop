from abc import ABC, abstractmethod
from typing import Dict
from src.modules.schedule.dto.schedule_dto import ScheduleDTO

class InterfaceScheduleCreateUsecase(ABC):

    @abstractmethod
    async def create(self, schedule: ScheduleDTO) -> Dict: pass