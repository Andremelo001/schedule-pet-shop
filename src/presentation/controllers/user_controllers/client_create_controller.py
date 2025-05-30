from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user.domain.use_cases.interface_client_create import InterfaceClientCreate
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.modules.user.dto.client_dto import ClientDTO

class ClientCreateController(ControllerInterface):
    def __init__(self, use_case: InterfaceClientCreate):
        self.use_case = use_case
        
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse:

        name = http_request.body["name"]
        cpf = http_request.body["cpf"]
        age = http_request.body["age"]
        email = http_request.body["email"]
        senha = http_request.body["senha"]

        client = ClientDTO(
            name=name,
            cpf=cpf,
            age=age,
            email=email,
            senha=senha
        )

        response = await self.use_case.create(session, client)

        return HttpResponse(
            status_code=200,
            body= {
                "data": response
            }
        )
