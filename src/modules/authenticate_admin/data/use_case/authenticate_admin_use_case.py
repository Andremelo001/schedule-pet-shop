from src.modules.authenticate_admin.domain.use_cases.interface_authenticate_admin_use_case import InterfaceAuthenticateAdminUseCase
from src.infra.db.repositories.admin_repository import AdminRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.drivers.jwt.jwt_service import JWTService
from src.drivers.password_hasher.password_hasher import PasswordHasher
from src.errors.error_handler import HttpUnauthorized

class AutheticateAdminUseCase(InterfaceAuthenticateAdminUseCase):
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    async def generate_token_admin(self, session: AsyncSession, senha: str, user: str) -> str:
        jwt_service = JWTService()

        await self.verify_user(session, senha, user)
        
        return jwt_service.create_token({"sub": senha})
    
    async def verify_user(self, session: AsyncSession, senha: str, user: str) -> None:

        verify_senha = PasswordHasher()
        
        admin = await self.repository.get_admin_by_user(session, user)

        if not admin or not verify_senha.verify(senha, admin.senha):
            raise HttpUnauthorized("Invalid email or password")