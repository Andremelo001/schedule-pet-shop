from typing import Dict
from src.modules.service_types.domain.use_cases.interface_service_delete import InterfaceServiceDelete
from src.modules.service_types.data.interfaces.interface_service_repository import InterfaceServiceRepository

from src.errors.error_handler import HttpNotFoundError, HttpUnauthorized

class ServiceDeleteUseCase(InterfaceServiceDelete):
    def __init__(self, repository: InterfaceServiceRepository):
        self.__repository = repository
    
    async def delete(self, id_service: str) -> Dict:

        await self.__service_not_found(id_service)

        await self.__already_exists_schedules_by_service_id(id_service)

        await self.__repository.delete_service(id_service)

        return {"message": "Serviço deletado com sucesso"}

    async def __service_not_found(self, id_service: str) -> None:

        service = await self.__repository.find_service_by_id(id_service)

        if not service:
            raise HttpNotFoundError(f"Serviço com o id {id_service} não encontrado")
        
    async def __already_exists_schedules_by_service_id(self, id_service: str) -> None:

        schedules = await self.__repository.get_schedules_by_service_id(id_service)

        for schedule in schedules:
            if schedule:
                raise HttpUnauthorized("Serviço não pode ser deletado, pois à agendamentos cadastrados com esse serviço!")
