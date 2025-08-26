from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.drivers.jwt.jwt_service import JWTService
from src.modules.schedule.domain.use_cases.interface_request_cancel_schedule import InterfaceRequestCancelScheduleUsecase
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository

from src.errors.error_handler import HttpNotFoundError

class RequestCancelScheduleUseCase(InterfaceRequestCancelScheduleUsecase):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.repository = repository

    async def request_cancel(self, session: AsyncSession, id_schedule: str) -> Dict:

        jwt_service = JWTService()

        await self.__schedule_already_exists(session, id_schedule)

        token = jwt_service.create_token({"sub": id_schedule, "role": ["request_cancel_schedule", "admin"]})

        return self.__format_response(id_schedule, token)
    
    async def __schedule_already_exists(self, session: AsyncSession, id_schedule: str) -> None:

        schedule = await self.repository.find_schedule_by_id(session, id_schedule)

        if not schedule:
            raise HttpNotFoundError(f"Agendamento com o id {id_schedule} não encontrado")
    
    @classmethod
    def __format_response(cls, id_schedule: str, token: str) -> Dict:

        return {
            "id_schedule": id_schedule,
            "token": token
        }