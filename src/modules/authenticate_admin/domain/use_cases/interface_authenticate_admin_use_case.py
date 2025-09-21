from abc import ABC, abstractmethod

class InterfaceAuthenticateAdminUseCase(ABC):
    @abstractmethod
    async def generate_token_admin(self, senha: str, user: str) -> str: pass