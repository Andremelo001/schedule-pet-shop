from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.service_types.domain.use_cases.interface_service_delete import InterfaceServiceDelete
from src.modules.service_types.data.interfaces.interface_service_repository import InterfaceServiceRepository

from src.errors.error_handler import HttpNotFoundError, HttpUnauthorized

class ServiceDeleteUseCase(InterfaceServiceDelete):
    def __init__(self, repository: InterfaceServiceRepository):
        self.repository = repository
    
    async def delete(self, session: AsyncSession, id_service: str) -> None:

        await self.__service_not_found(session, id_service)

        await self.__already_exists_schedules_by_service_id(session, id_service)

        await self.repository.delete_service(session, id_service)

        return {"message": "Serviço deletado com sucesso"}

    async def __service_not_found(self, session: AsyncSession, id_service: str) -> None:

        service = await self.repository.find_service_by_id(session, id_service)

        if not service:
            raise HttpNotFoundError(f"Serviço com o id {id_service} não encontrado")
        
    async def __already_exists_schedules_by_service_id(self, session: AsyncSession, id_service: str) -> None:

        schedules = await self.repository.get_schedules_by_service_id(session, id_service)

        for schedule in schedules:
            if schedule:
                raise HttpUnauthorized("Serviço não pode ser deletado, pois à agendamentos cadastrados com esse serviço!")
