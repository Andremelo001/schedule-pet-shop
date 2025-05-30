from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.authenticate_user.domain.use_cases.interface_authenticate_user_use_case import InterfaceAuthentivcateUserUseCase
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class GenerateTokenController(ControllerInterface):
    def __init__(self, use_case: InterfaceAuthentivcateUserUseCase):
        self.use_case = use_case

    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        email = http_request.body["email"]
        senha = http_request.body["senha"]

        responde = await self.use_case.generate_token(session, email, senha)

        return HttpResponse(
            status_code=200,
            body= {
                "token": responde
            }
        )