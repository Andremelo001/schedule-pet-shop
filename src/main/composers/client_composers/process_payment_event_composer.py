# src/main/composers/client_composers/process_payment_event_composer.py
from src.modules.user.data.use_cases.process_payment_use_case import ProcessPaymentUseCase
from src.presentation.controllers.user_controllers.process_payment_event_controller import ProcessPaymentEventController
from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.infra.db.settings.connection import DBConection

db = DBConection()

async def process_payment_event_composer(message_body: dict):
    async with db.get_session() as session:
        repository = ScheduleRepository(session)

        use_case = ProcessPaymentUseCase(repository)

        controller = ProcessPaymentEventController(use_case)

        return await controller.handle(message_body)