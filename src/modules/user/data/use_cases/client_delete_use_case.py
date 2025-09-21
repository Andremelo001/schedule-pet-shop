from typing import Dict
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.domain.use_cases.interface_client_delete import InterfaceClientDelete

from src.errors.error_handler import HttpNotFoundError, HttpUnauthorized

class ClientDeleteUseCase(InterfaceClientDelete):
    def __init__(self, repositoy: InterfaceClientRepository):
        self.__repository = repositoy

    async def delete(self, id_client: str) -> Dict:

        await self.__client_not_found(id_client)

        await self.__verify_if_clients_has_schedules_actives(id_client)

        await self.__repository.delete_client(id_client)

        return {"message": "Cliente deletado com sucesso do banco de dados"}
    
    async def __client_not_found(self, id_client: str):

        client = await self.__repository.get_client_by_id(id_client)

        if not client:
            raise HttpNotFoundError(f"Cliente com o id {id_client} não encontrado")
        
    async def __verify_if_clients_has_schedules_actives(self, id_client: str) -> None:

        schedules = await self.__repository.find_schedule_by_id_client(id_client)

        for schedule in schedules:
            if schedule.schedule_active == True:
                raise HttpUnauthorized("Não é possivel deletar o cliente, pois ele apresenta agendamentos ativos")
