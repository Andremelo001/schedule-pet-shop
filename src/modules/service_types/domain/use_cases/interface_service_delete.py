from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

class InterfaceServiceDelete(ABC):

    @abstractmethod
    async def delete(self, session: AsyncSession, id_service: str) -> None: pass