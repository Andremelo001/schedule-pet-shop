from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.user.domain.use_cases.interface_client_delete import InterfaceClientDelete
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.http_types.http_request import HttpRequest

class ClientDeleteController(ControllerInterface):
    def __init__(self, use_case: InterfaceClientDelete):
        self.__use_case = use_case

    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        id_client = http_request.query_params["id_client"]

        response = await self.__use_case.delete(id_client)

        return HttpResponse(
            status_code=200,
            body = {
                "data": response
            }
        )