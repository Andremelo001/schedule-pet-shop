from typing import List, Dict
from src.modules.service_types.domain.use_cases.interface_service_list import InterfaceServiceList
from src.modules.service_types.data.interfaces.interface_service_repository import InterfaceServiceRepository
from src.modules.service_types.domain.models.service import Service

class ServiceListUseCase(InterfaceServiceList):
    def __init__(self, repository: InterfaceServiceRepository):
        self.__repository = repository
    
    async def list(self) -> List[Dict]:

        services = await self.__repository.list_services()

        return self.__format_response(services)

    @classmethod
    def __format_response(cls, services: List[Service]) -> List[Dict]:

        return [{
            "id": str(service.id),
            "duration_in_minutes": service.duration_in_minutes,
            "type_service": service.type_service,
            "price": service.price,
        } for service in services]