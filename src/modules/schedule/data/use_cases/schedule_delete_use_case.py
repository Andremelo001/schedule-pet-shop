from typing import Dict
from datetime import date
from src.errors.error_handler import HttpUnauthorized, HttpNotFoundError
from src.modules.schedule.domain.use_cases.interface_schedule_delete import InterfaceScheduleDeleteUsecase
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository

class ScheduleDeleteUseCase(InterfaceScheduleDeleteUsecase):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.__repository = repository

    async def delete(self, id_schedule: str) -> Dict:

        await self.__schedule_not_found(id_schedule)

        await self.__verify_schedule_date_has_passed(id_schedule)

        await self.__repository.delete_schedule(id_schedule)

        return {"message": "Agendamento deletado com sucesso"}

    
    async def __schedule_not_found(self, id_schedule: str) -> None:

        schedule = await self.__repository.find_schedule_by_id(id_schedule)

        if not schedule:
            raise HttpNotFoundError(f"Agendamento com o id {id_schedule} não encontrado!")
        
    async def __verify_schedule_date_has_passed(self, id_schedule: str) -> None:

        schedule = await self.__repository.find_schedule_by_id(id_schedule)

        current_date = date.today()

        if schedule.date_schedule > current_date:
            raise HttpUnauthorized("Não é possivel excluir o agendamento, pois o agendamento ainda não aconteceu!")
        
