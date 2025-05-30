from sqlalchemy.ext.asyncio import AsyncSession

from abc import ABC, abstractmethod

class InterfaceAuthentivcateUserUseCase(ABC):

    @abstractmethod
    async def generate_token(self, session: AsyncSession, email: str, senha: str) -> str: pass
