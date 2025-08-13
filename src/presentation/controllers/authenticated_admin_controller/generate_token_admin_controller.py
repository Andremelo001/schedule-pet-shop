from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.authenticate_admin.domain.use_cases.interface_authenticate_admin_use_case import InterfaceAuthenticateAdminUseCase
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class GenerateTokenAdminController(ControllerInterface):
    def __init__(self, use_case: InterfaceAuthenticateAdminUseCase):
        self.use_case = use_case

    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        senha = http_request.body["senha"]
        user = http_request.body["user"]

        responde = await self.use_case.generate_token_admin(session, senha, user)

        return HttpResponse(
            status_code=200,
            body= {
                "message": "Administrador do Sistema autenticado com sucesso",
                "token": responde
            }
        )