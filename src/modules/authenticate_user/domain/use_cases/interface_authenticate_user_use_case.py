from abc import ABC, abstractmethod

class InterfaceAuthentivcateUserUseCase(ABC):

    @abstractmethod
    async def generate_token(self, email: str, senha: str) -> str: pass
