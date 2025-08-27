from sqlalchemy.ext.asyncio import AsyncSession

from typing import Dict

from src.modules.service_types.data.interfaces.interface_service_repository import InterfaceServiceRepository
from src.modules.service_types.domain.use_cases.interface_service_update import InterfaceServiceUpdate
from src.modules.service_types.dto.service_dto import UpdateServiceDTO
from src.modules.service_types.domain.models.type_service import TypeService

from src.modules.service_types.domain.models.service import Service

from src.errors.error_handler import HttpUnauthorized, HttpNotFoundError

class ServiceUpdateUseCase(InterfaceServiceUpdate):
    def __init__(self, repository: InterfaceServiceRepository):
        self.repository = repository

    async def update(self, session: AsyncSession, service: UpdateServiceDTO, id_service: str) -> Dict:

        if service.type_service is not None:
            self.__validate_type_service(service.type_service)

        await self.__validate_service_in_schedule(session, id_service)

        await self.__service_already_exists(session, id_service)

        new_service = await self.repository.update_service(session, service, id_service)

        return self.__format_response(new_service)

    @classmethod
    def __validate_type_service(cls, type_service: str) -> None:
        
        valid_services = [service.value for service in TypeService]
        
        if type_service not in valid_services:
            raise HttpUnauthorized(f"Tipo de serviço não aceito, escolha um dos serviços disponíveis: {', '.join(valid_services)}")
        
    async def __service_already_exists(self, session: AsyncSession, id_service: str) -> None:

        service = await self.repository.find_service_by_id(session, id_service)

        if not service:
            raise HttpNotFoundError("Serviço não encontrado em nossa base de dados")
        
    async def __validate_service_in_schedule(self, session: AsyncSession, id_service: str) -> None:

        schedules = await self.repository.get_schedules_by_service_id(session, id_service)

        for schedule in schedules:
            if schedule:
                raise HttpUnauthorized(f"Não é possivel atualizar o serviço com id {id_service}, pois existe um agendamento com esse serviço")
            
    @classmethod
    def __format_response(cls, service: Service) -> Dict:

        return {
            "id": str(service.id),
            "duration_in_minutes": service.duration_in_minutes,
            "type_service": service.type_service,
            "price": service.price
        }