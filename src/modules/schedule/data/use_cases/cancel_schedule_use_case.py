from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.modules.schedule.domain.use_cases.interface_cancel_schedule import InterfaceCancelScheduleUsecase
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository

from src.drivers.email_sender.email_service import EmailService

from src.drivers.email_sender.dto.mail_body_dto import MailBody


class CancelScheduleUseCase(InterfaceCancelScheduleUsecase):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.repository = repository


    async def cancel(self, session: AsyncSession, id_schedule: str) -> Dict:

        await self.repository.cancel_schedule(session, id_schedule)

        await self.send_email_for_client(session, id_schedule)

        return {"message": "Agendamento cancelado com sucesso"}


    async def send_email_for_client(self, session: AsyncSession, id_schedule: str) -> None:

        email_service = EmailService()

        email = await self.repository.find_email_client_by_id_schedule(session, id_schedule)

        # Monta e-mail para o cliente
        mail_body = MailBody(
            to=email,
            subject="Cancelamento de Agendamento",
            body=f"Olá, seu agendamento {id_schedule} foi cancelado com sucesso."
        )

        email_service.send_email(mail_body.model_dump())