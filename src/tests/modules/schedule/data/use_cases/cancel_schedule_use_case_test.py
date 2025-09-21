import pytest
from unittest.mock import AsyncMock, patch

from src.modules.schedule.data.use_cases.cancel_schedule_use_case import CancelScheduleUseCase


@pytest.mark.asyncio
async def test_cancel_schedule_success(mocker):
    mock_repository = AsyncMock()

    # Mock email found
    mock_repository.find_email_client_by_id_schedule.return_value = "client@example.com"

    # Mock EmailService
    with patch('src.modules.schedule.data.use_cases.cancel_schedule_use_case.EmailService') as mock_email_service_class:
        mock_email_service_instance = mock_email_service_class.return_value

        # Mock MailBody
        with patch('src.modules.schedule.data.use_cases.cancel_schedule_use_case.MailBody') as mock_mail_body_class:
            mock_mail_body_instance = mock_mail_body_class.return_value
            mock_mail_body_instance.model_dump.return_value = {
                "to": "client@example.com",
                "subject": "Cancelamento de Agendamento",
                "body": "Olá, seu agendamento schedule-id-123 foi cancelado com sucesso."
            }

            use_case = CancelScheduleUseCase(mock_repository)
            result = await use_case.cancel( "schedule-id-123")

            assert result["message"] == "Agendamento cancelado com sucesso"

            mock_repository.cancel_schedule.assert_called_once_with( "schedule-id-123")
            mock_repository.find_email_client_by_id_schedule.assert_called_once_with( "schedule-id-123")

            # Verify email was sent
            mock_email_service_instance.send_email.assert_called_once_with({
                "to": "client@example.com",
                "subject": "Cancelamento de Agendamento",
                "body": "Olá, seu agendamento schedule-id-123 foi cancelado com sucesso."
            })

            # Verify MailBody was created correctly
            mock_mail_body_class.assert_called_once_with(
                to="client@example.com",
                subject="Cancelamento de Agendamento",
                body="Olá, seu agendamento schedule-id-123 foi cancelado com sucesso."
            )


@pytest.mark.asyncio
async def test_cancel_schedule_with_different_email(mocker):
    mock_repository = AsyncMock()

    # Mock different email found
    mock_repository.find_email_client_by_id_schedule.return_value = "another@example.com"

    # Mock EmailService
    with patch('src.modules.schedule.data.use_cases.cancel_schedule_use_case.EmailService') as mock_email_service_class:
        mock_email_service_instance = mock_email_service_class.return_value

        # Mock MailBody
        with patch('src.modules.schedule.data.use_cases.cancel_schedule_use_case.MailBody') as mock_mail_body_class:
            mock_mail_body_instance = mock_mail_body_class.return_value
            mock_mail_body_instance.model_dump.return_value = {
                "to": "another@example.com",
                "subject": "Cancelamento de Agendamento",
                "body": "Olá, seu agendamento schedule-id-456 foi cancelado com sucesso."
            }

            use_case = CancelScheduleUseCase(mock_repository)
            result = await use_case.cancel( "schedule-id-456")

            assert result["message"] == "Agendamento cancelado com sucesso"

            mock_repository.cancel_schedule.assert_called_once_with( "schedule-id-456")
            mock_repository.find_email_client_by_id_schedule.assert_called_once_with( "schedule-id-456")

            # Verify email was sent with correct email
            mock_email_service_instance.send_email.assert_called_once_with({
                "to": "another@example.com",
                "subject": "Cancelamento de Agendamento",
                "body": "Olá, seu agendamento schedule-id-456 foi cancelado com sucesso."
            })


@pytest.mark.asyncio
async def test_send_email_for_client_only(mocker):
    mock_repository = AsyncMock()

    # Mock email found
    mock_repository.find_email_client_by_id_schedule.return_value = "test@example.com"

    # Mock EmailService
    with patch('src.modules.schedule.data.use_cases.cancel_schedule_use_case.EmailService') as mock_email_service_class:
        mock_email_service_instance = mock_email_service_class.return_value

        # Mock MailBody
        with patch('src.modules.schedule.data.use_cases.cancel_schedule_use_case.MailBody') as mock_mail_body_class:
            mock_mail_body_instance = mock_mail_body_class.return_value
            mock_mail_body_instance.model_dump.return_value = {
                "to": "test@example.com",
                "subject": "Cancelamento de Agendamento",
                "body": "Olá, seu agendamento test-id foi cancelado com sucesso."
            }

            use_case = CancelScheduleUseCase(mock_repository)
            # Test only the email sending method
            await use_case.send_email_for_client( "test-id")

            mock_repository.find_email_client_by_id_schedule.assert_called_once_with( "test-id")
            mock_email_service_instance.send_email.assert_called_once()
