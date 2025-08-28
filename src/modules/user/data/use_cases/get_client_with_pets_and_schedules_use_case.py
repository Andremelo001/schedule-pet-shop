from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.modules.user.domain.use_cases.interface_get_client_with_pets_and_schedules import InterfaceGetClientWithPetsAndSchedules
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.infra.db.entities.client import ClientWithPetsWithSchedules

from src.errors.error_handler import HttpNotFoundError

class GetClientWithPetsAndSchedulesUseCase(InterfaceGetClientWithPetsAndSchedules):
    def __init__(self, repository: InterfaceClientRepository):
        self.repository = repository

    async def get_client_with_pets_and_schedules(self, session: AsyncSession, id_client: str) -> Dict:

        await self.__client_not_found(session, id_client)

        client = await self.repository.get_client_with_pets_and_schedules_by_id(session, id_client)

        return self.__format_response(client)

    async def __client_not_found(self, session: AsyncSession, id_client: str):

        client = await self.repository.get_client_by_id(session, id_client)

        if not client:
            raise HttpNotFoundError(f"Cliente com o id {id_client} não encontrado")
        
    @classmethod
    def __format_response(cls, client: ClientWithPetsWithSchedules) -> Dict:

        return {
            "id": str(client.id),
            "name": client.name,
            "cpf": client.cpf,
            "age": client.age,
            "email": client.email,
            "pets": [
                {
                    "id": str(pet.id),
                    "name": pet.name,
                    "breed": pet.breed,
                    "age": pet.age,
                    "size_in_centimeters": pet.size_in_centimeters
                }
                for pet in client.pets
            ],
            "schedules": [
                {
                    "id": str(schedule.id),
                    "date_schedule": str(schedule.date_schedule),
                    "time_schedule": str(schedule.time_schedule),
                    "total_price_schedule": schedule.total_price_schedule,
                    "schedule_active": schedule.schedule_active

                }
                for schedule in client.schedules
            ]
        }