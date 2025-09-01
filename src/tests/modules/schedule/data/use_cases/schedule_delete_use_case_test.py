import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date

from src.modules.schedule.data.use_cases.schedule_delete_use_case import ScheduleDeleteUseCase
from src.errors.types_errors.http_not_found import HttpNotFoundError
from src.errors.types_errors.http_Unauthorized import HttpUnauthorized


@pytest.mark.asyncio
async def test_delete_schedule_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedule exists and date has passed
    fake_schedule = MagicMock()
    fake_schedule.id = "schedule-id-123"
    fake_schedule.date_schedule = date(2024, 1, 15)  # Data no passado
    mock_repository.find_schedule_by_id.return_value = fake_schedule

    # Mock current date
    with patch('src.modules.schedule.data.use_cases.schedule_delete_use_case.date') as mock_date:
        mock_date.today.return_value = date(2024, 8, 29)  # Data atual
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        use_case = ScheduleDeleteUseCase(mock_repository)
        result = await use_case.delete(mock_session, "schedule-id-123")

        assert result["message"] == "Agendamento deletado com sucesso"

        # Verify that find_schedule_by_id was called twice (once for validation, once for date check)
        assert mock_repository.find_schedule_by_id.call_count == 2
        mock_repository.find_schedule_by_id.assert_any_call(mock_session, "schedule-id-123")
        mock_repository.delete_schedule.assert_called_once_with(mock_session, "schedule-id-123")


@pytest.mark.asyncio
async def test_delete_schedule_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedule does not exist
    mock_repository.find_schedule_by_id.return_value = None

    use_case = ScheduleDeleteUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError, match="Agendamento com o id schedule-id-nonexistent não encontrado!"):
        await use_case.delete(mock_session, "schedule-id-nonexistent")

    mock_repository.find_schedule_by_id.assert_called_once_with(mock_session, "schedule-id-nonexistent")


@pytest.mark.asyncio
async def test_delete_schedule_future_date(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedule exists but date is in the future
    fake_schedule = MagicMock()
    fake_schedule.id = "schedule-id-123"
    fake_schedule.date_schedule = date(2024, 12, 25)  # Data no futuro
    mock_repository.find_schedule_by_id.return_value = fake_schedule

    # Mock current date
    with patch('src.modules.schedule.data.use_cases.schedule_delete_use_case.date') as mock_date:
        mock_date.today.return_value = date(2024, 8, 29)  # Data atual
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        use_case = ScheduleDeleteUseCase(mock_repository)

        with pytest.raises(HttpUnauthorized, match="Não é possivel excluir o agendamento, pois o agendamento ainda não aconteceu!"):
            await use_case.delete(mock_session, "schedule-id-123")

        # Verify that find_schedule_by_id was called twice (once for validation, once for date check)
        assert mock_repository.find_schedule_by_id.call_count == 2
        mock_repository.find_schedule_by_id.assert_any_call(mock_session, "schedule-id-123")


@pytest.mark.asyncio
async def test_delete_schedule_same_date(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedule exists and date is today (should allow deletion)
    fake_schedule = MagicMock()
    fake_schedule.id = "schedule-id-123"
    fake_schedule.date_schedule = date(2024, 8, 29)  # Data de hoje
    mock_repository.find_schedule_by_id.return_value = fake_schedule

    # Mock current date
    with patch('src.modules.schedule.data.use_cases.schedule_delete_use_case.date') as mock_date:
        mock_date.today.return_value = date(2024, 8, 29)  # Data atual
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        use_case = ScheduleDeleteUseCase(mock_repository)
        result = await use_case.delete(mock_session, "schedule-id-123")

        assert result["message"] == "Agendamento deletado com sucesso"

        # Verify that find_schedule_by_id was called twice (once for validation, once for date check)
        assert mock_repository.find_schedule_by_id.call_count == 2
        mock_repository.find_schedule_by_id.assert_any_call(mock_session, "schedule-id-123")
        mock_repository.delete_schedule.assert_called_once_with(mock_session, "schedule-id-123")
