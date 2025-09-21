from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.drivers.jwt.jwt_service import JWTService
from src.drivers.password_hasher.password_hasher import PasswordHasher
from src.errors.types_errors import HttpUnauthorized
from src.modules.authenticate_user.domain.use_cases.interface_authenticate_user_use_case import InterfaceAuthentivcateUserUseCase


class AuthenticateUserUseCase(InterfaceAuthentivcateUserUseCase):
    def __init__(self, repository: InterfaceClientRepository):
        self.__repository = repository


    async def generate_token(self, email: str, senha: str) -> str:

        jwt_service = JWTService()

        await self.verify_user(email, senha)
        
        return jwt_service.create_token({"sub": senha, "role": "client"})
    
    async def verify_user(self, email: str, senha: str) -> None:

        verify_senha = PasswordHasher()
        
        user = await self.__repository.get_client_by_email(email)

        if not user or not verify_senha.verify(senha, user.senha):
            raise HttpUnauthorized("Invalid email or password")




