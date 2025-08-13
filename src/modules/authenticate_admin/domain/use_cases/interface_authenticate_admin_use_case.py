from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceAuthenticateAdminUseCase(ABC):
    @abstractmethod
    async def generate_token_admin(self, session: AsyncSession, senha: str, user: str) -> str: pass