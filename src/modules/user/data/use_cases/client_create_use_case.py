import re
from typing import Dict

from src.modules.user.domain.use_cases.interface_client_create import InterfaceClientCreate
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.dto.client_dto import ClientDTO
from src.modules.user.data.use_cases.client_finder_use_case import ClientFinderUseCase
from src.drivers.password_hasher.password_hasher import PasswordHasher

from src.errors.types_errors import HttpBadRequestError, HttpConflitError


class CreateClientUseCase(InterfaceClientCreate):
    def __init__(self, repository: InterfaceClientRepository):
        self.__repository = repository

    async def create(self, client: ClientDTO) -> Dict:

        await self.__client_exists(client.cpf)
        
        self.validate_email(client.email)

        self.validate_senha(client.senha)

        client.senha = self.encrypt_senha(client.senha)

        client.cpf = self.format_cpf(client.cpf)

        return await self.__register_client_informations(client)

    @classmethod
    def validate_email(cls, email: str) -> None:
        email_padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.match(email_padrao, email):
            raise HttpBadRequestError("O e-mail informado não é válido! Exemplo: ex@gmail.com")
        
    @classmethod
    def validate_senha(cls, senha: str) -> None:
        if not bool(re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha)):
            raise HttpBadRequestError("A senha deve conter pelo menos uma letra maiúscula, um número e ter no mínimo 8 caracteres")
        
    @classmethod
    def encrypt_senha(cls, senha: str) -> str:

        password_hasher = PasswordHasher()

        pass_encrypt = password_hasher.hash(senha)

        return pass_encrypt
        
    @classmethod
    def format_cpf(cls, cpf_client) -> str:

        return ClientFinderUseCase.validate_cpf(cpf_client)

    async def __client_exists(self, cpf: str) -> None:
        client_exists = await self.__repository.get_client(cpf)

        if client_exists:
            raise HttpConflitError(f"Cliente com o cpf {cpf} já existe")
        
    async def __register_client_informations(self, client: ClientDTO) -> Dict:
        await self.__repository.create_client(client)

        return {"message": "Cliente cadastrado com sucesso"}