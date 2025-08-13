import re
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.modules.user.domain.use_cases.interface_client_finder import InterfaceClientFinder
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.domain.models.client import Client

from src.errors.types_errors import HttpNotFoundError, HttpBadRequestError

class ClientFinderUseCase(InterfaceClientFinder):
    def __init__(self, client_repository: InterfaceClientRepository) -> None:
        self.__client_repository = client_repository

    async def find(self, session: AsyncSession, cpf_client: str) -> Dict:

        cpf_client = self.validate_cpf(cpf_client)

        client = await self.__find_client(session, cpf_client)

        return self.__format_response(client)
    
    @classmethod
    def validate_cpf(cls, cpf: str) -> str:
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)
        
        if len(cpf) != 11:
            raise HttpBadRequestError("Cpf informado não apresenta 11 dígitos")
        
        if cpf == cpf[0] * 11:
            raise HttpBadRequestError("Cpf informado apresenta todos os dígitos iguais")
        
        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        
        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        
        if cpf[-2:] != f"{digito1}{digito2}":
            raise HttpBadRequestError("Cpf informado é inválido")
        
        return cpf
    
    @classmethod
    def __format_response(cls, client: Client) -> Dict:
        
        response = []

        response.append(
            {
                "id": str(client.id),
                "name": client.name,
                "age": client.age,
                "email": client.email,
                "senha": client.senha
            }
        )

        return response
        
    async def __find_client(self, session: AsyncSession, cpf_client: str) -> Client:
        client = await self.__client_repository.get_client(session, cpf_client)

        if not client:
            raise HttpNotFoundError(f"Nenhum cliente encontrado com o cpf {cpf_client}")
        
        return client