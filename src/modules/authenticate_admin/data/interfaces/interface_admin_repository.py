from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.authenticate_admin.domain.models.admin import Admin

class InterfaceAdminRepository(ABC):

    @abstractmethod
    async def get_admin_by_user(cls, session: AsyncSession, user: str) -> Admin: pass