from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.schedule.dto.schedule_dto import ScheduleDTO

class InterfaceScheduleCreateUsecase(ABC):

    @abstractmethod
    async def create(self, session: AsyncSession, schedule: ScheduleDTO) -> Dict: pass