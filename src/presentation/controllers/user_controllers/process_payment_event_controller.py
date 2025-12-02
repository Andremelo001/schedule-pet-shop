from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interfaces.message_controller_interface import MessageControllerInterface
from src.modules.user.domain.use_cases.interface_process_payment import InterfaceProcessPayment

class ProcessPaymentEventController(MessageControllerInterface):
    def __init__(self, use_case: InterfaceProcessPayment):
        self.__use_case = use_case

    async def handle(self, message_body: dict) -> HttpResponse:

        status = message_body.get("status")
        schedule_id = message_body.get("schedule_id")

        if not status or not schedule_id:
            return HttpResponse(
                status_code=400,
                body={
                    "confirmation": False,
                    "message": "Invalid message: missing status or schedule_id",
                    "received": message_body
                }
            )

        try:
            response = await self.__use_case.process_notification(schedule_id, status)

            return HttpResponse(
                status_code=200, 
                body=response
            )
        
        except Exception as e:
            return HttpResponse(
                status_code=500,
                body={
                    "confirmation": False,
                    "message": f"Error processing payment: {str(e)}",
                    "schedule_id": schedule_id
                }
            )
