from typing import Dict
from src.drivers.jwt.jwt_service import JWTService
from src.modules.schedule.domain.use_cases.interface_request_cancel_schedule import InterfaceRequestCancelScheduleUsecase
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository

from src.errors.error_handler import HttpNotFoundError

class RequestCancelScheduleUseCase(InterfaceRequestCancelScheduleUsecase):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.__repository = repository

    async def request_cancel(self, id_schedule: str) -> Dict:

        jwt_service = JWTService()

        await self.__schedule_not_found(id_schedule)

        token = jwt_service.create_token({"sub": id_schedule, "role": ["request_cancel_schedule", "admin"]})

        return self.__format_response(id_schedule, token)
    
    async def __schedule_not_found(self, id_schedule: str) -> None:

        schedule = await self.__repository.find_schedule_by_id(id_schedule)

        if not schedule:
            raise HttpNotFoundError(f"Agendamento com o id {id_schedule} não encontrado")
    
    @classmethod
    def __format_response(cls, id_schedule: str, token: str) -> Dict:

        return {
            "id_schedule": id_schedule,
            "token": token
        }