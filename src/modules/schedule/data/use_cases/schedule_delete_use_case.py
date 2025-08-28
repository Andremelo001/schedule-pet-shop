from typing import Dict
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.errors.error_handler import HttpUnauthorized, HttpNotFoundError

from src.modules.schedule.domain.use_cases.interface_schedule_delete import InterfaceScheduleDeleteUsecase
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository

class ScheduleDeleteUseCase(InterfaceScheduleDeleteUsecase):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.repository = repository

    async def delete(self, session: AsyncSession, id_schedule: str) -> Dict:

        await self.__schedule_not_found(session, id_schedule)

        await self.__verify_schedule_date_has_passed(session, id_schedule)

        await self.repository.delete_schedule(session, id_schedule)

        return {"message": "Agendamento deletado com sucesso"}

    
    async def __schedule_not_found(self, session: AsyncSession, id_schedule: str) -> None:

        schedule = await self.repository.find_schedule_by_id(session, id_schedule)

        if not schedule:
            raise HttpNotFoundError(f"Agendamento com o id {id_schedule} não encontrado!")
        
    async def __verify_schedule_date_has_passed(self, session: AsyncSession, id_schedule: str) -> None:

        schedule = await self.repository.find_schedule_by_id(session, id_schedule)

        current_date = date.today()

        if schedule.date_schedule > current_date:
            raise HttpUnauthorized("Não é possivel excluir o agendamento, pois o agendamento ainda não aconteceu!")
        
