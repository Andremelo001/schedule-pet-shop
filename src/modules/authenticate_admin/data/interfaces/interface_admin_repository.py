from abc import ABC, abstractmethod
from src.modules.authenticate_admin.domain.models.admin import Admin

class InterfaceAdminRepository(ABC):

    @abstractmethod
    async def get_admin_by_user(self, user: str) -> Admin: pass