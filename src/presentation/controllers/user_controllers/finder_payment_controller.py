from src.presentation.interfaces.controller_interface import ControllerInterface
from src.modules.user.domain.use_cases.interface_finder_payment import InterfaceFinderPayment
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FinderPaymentController(ControllerInterface):
    def __init__(self, use_case: InterfaceFinderPayment):
        self.__use_case = use_case

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        
        id_schedule = http_request.query_params["id_schedule"]

        response = await self.__use_case.finder_payment(id_schedule)

        return HttpResponse(
            status_code=200,
             body= {
                 "data": response
             }
        )