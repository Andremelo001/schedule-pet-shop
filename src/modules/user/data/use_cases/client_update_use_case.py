from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.modules.user.domain.use_cases.interface_client_update import InterfaceClientUpdate
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.data.use_cases.client_create_use_case import CreateClientUseCase
from src.modules.user.dto.client_dto import ClientUpdateDTO
from src.modules.user.domain.models.client import Client

from src.errors.types_errors import HttpConflitError

class ClientUpdateUseCase(InterfaceClientUpdate):
    def __init__(self, repository: InterfaceClientRepository):
        self.repository = repository

    async def update(self, session: AsyncSession, id_client: str, client: ClientUpdateDTO) -> Dict:

        if client.cpf is not None:
            await self.__client_exists(session, client.cpf, id_client)

            client.cpf = self.__format_cpf(client.cpf)
            
        if client.email is not None:
            self.__validate_email(client.email)

        if client.senha is not None:
            self.__validate_senha(client.senha)

        new_client = await self.repository.update_client(session, id_client, client)
    
        return self.__format_response(new_client)

    
    async def __client_exists(self, session: AsyncSession, cpf: str, id_client: str) -> None:
        client = await self.repository.get_client(session, cpf)

        if client and str(client.id) != id_client:
            raise HttpConflitError(f"Cliente com o cpf {cpf} já existe")

    @classmethod
    def __validate_email(cls, email: str) -> None:
        if email is not None:
            CreateClientUseCase.validate_email(email)

    @classmethod
    def __validate_senha(cls, senha: str) -> None:
        if senha is not None:
            CreateClientUseCase.validate_senha(senha)
        
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
    