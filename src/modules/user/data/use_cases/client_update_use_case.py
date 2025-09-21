from typing import Dict

from src.modules.user.domain.use_cases.interface_client_update import InterfaceClientUpdate
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.data.use_cases.client_create_use_case import CreateClientUseCase
from src.modules.user.dto.client_dto import ClientUpdateDTO
from src.modules.user.domain.models.client import Client

from src.errors.types_errors import HttpConflitError, HttpNotFoundError

class ClientUpdateUseCase(InterfaceClientUpdate):
    def __init__(self, repository: InterfaceClientRepository):
        self.__repository = repository

    async def update(self, id_client: str, client: ClientUpdateDTO) -> Dict:

        await self.__client_not_found(id_client)

        if client.cpf is not None:
            await self.__client_exists(client.cpf, id_client)

            client.cpf = self.__format_cpf(client.cpf)

        new_client = await self.__repository.update_client(id_client, client)
    
        return self.__format_response(new_client)
    

    async def __client_not_found(self, id_client: str):

        client = await self.__repository.get_client_by_id(id_client)

        if not client:
            raise HttpNotFoundError(f"Cliente com o id {id_client} não encontrado")

    
    async def __client_exists(self, cpf: str, id_client: str) -> None:

        client = await self.__repository.get_client(cpf)

        if client and str(client.id) != id_client:
            raise HttpConflitError(f"Cliente com o cpf {cpf} já existe")
        
    @classmethod
    def __format_cpf(cls, cpf) -> str:

        if cpf is not None:
            return CreateClientUseCase.format_cpf(cpf)

    @classmethod
    def __format_response(cls, client: Client) -> Dict:

        return {
            'id': str(client.id),
            'name': client.name,
            "cpf": client.cpf,
            'age': client.age,
            'email': client.email,
            'senha': client.senha,
        }
    