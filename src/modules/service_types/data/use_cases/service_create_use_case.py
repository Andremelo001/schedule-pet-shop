from typing import Dict
from src.modules.service_types.data.interfaces.interface_service_repository import InterfaceServiceRepository
from src.modules.service_types.domain.use_cases.interface_service_create import InterfaceServiceCreate
from src.modules.service_types.dto.service_dto import ServiceDTO
from src.modules.service_types.domain.models.type_service import TypeService

from src.errors.error_handler import HttpUnauthorized

class ServiceCreateUseCase(InterfaceServiceCreate):
    def __init__(self, repository: InterfaceServiceRepository):
        self.__repository = repository

    async def create(self, service: ServiceDTO) -> Dict:

        self.__validate_type_service(service.type_service)

        await self.__service_alread_exists(service)

        return await self.__register_service_informations(service)

    @classmethod
    def __validate_type_service(cls, type_service: str) -> None:
        
        valid_services = [service.value for service in TypeService]
        
        if type_service not in valid_services:
            raise HttpUnauthorized(f"Tipo de serviço não aceito, escolha um dos serviços disponíveis: {', '.join(valid_services)}")
        
     
    async def __service_alread_exists(self, service_dto: ServiceDTO) -> None:

        services = await self.__repository.list_services()

        for service in services:
            if (service.type_service == service_dto.type_service) and (service.price == service_dto.price):
                raise HttpUnauthorized("Serviço já existe no banco de dados")
    
    async def __register_service_informations(self, service: ServiceDTO) -> Dict:
        
        await self.__repository.create_service(service)

        return {"message": "Serviço cadastrado com sucesso"}

