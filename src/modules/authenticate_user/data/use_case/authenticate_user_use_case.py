from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.drivers.jwt.jwt_service import JWTService
from src.drivers.password_hasher.password_hasher import PasswordHasher
from src.errors.types_errors import HttpUnauthorized
from src.modules.authenticate_user.domain.use_cases.interface_authenticate_user_use_case import InterfaceAuthentivcateUserUseCase


class AuthenticateUserUseCase(InterfaceAuthentivcateUserUseCase):
    def __init__(self, repository: InterfaceClientRepository):
        self.repository = repository


    async def generate_token(self, session: AsyncSession, email: str, senha: str) -> str:

        jwt_service = JWTService()

        await self.verify_user(session, email, senha)
        
        return jwt_service.create_token({"sub": senha})
    
    async def verify_user(self, session: AsyncSession, email: str, senha: str) -> None:

        verify_senha = PasswordHasher()
        
        user = await self.repository.get_client_by_email(session, email)

        if not user or not verify_senha.verify(senha, user.senha):
            raise HttpUnauthorized("Invalid email or password")




