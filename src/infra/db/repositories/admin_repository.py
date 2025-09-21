from src.modules.authenticate_admin.data.interfaces.interface_admin_repository import InterfaceAdminRepository
from src.modules.authenticate_admin.domain.models.admin import Admin
from src.infra.db.entities.admin import Admin as AdminEntitie

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select

class AdminRepository(InterfaceAdminRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_admin_by_user(self, user: str) -> Admin:

        admin = await self.__session.execute(select(AdminEntitie).where(AdminEntitie.user == user))

        return admin.scalar_one_or_none()