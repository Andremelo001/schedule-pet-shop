import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.modules.schedule.data.use_cases.request_cancel_schedule_use_case import RequestCancelScheduleUseCase
from src.errors.types_errors.http_not_found import HttpNotFoundError


@pytest.mark.asyncio
async def test_request_cancel_schedule_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedule exists
    fake_schedule = MagicMock()
    fake_schedule.id = "schedule-id-123"
    mock_repository.find_schedule_by_id.return_value = fake_schedule

    # Mock JWT service
    with patch('src.modules.schedule.data.use_cases.request_cancel_schedule_use_case.JWTService') as mock_jwt_service_class:
        mock_jwt_service_instance = mock_jwt_service_class.return_value
        mock_jwt_service_instance.create_token.return_value = "fake_cancel_token"

        use_case = RequestCancelScheduleUseCase(mock_repository)
        result = await use_case.request_cancel(mock_session, "schedule-id-123")

        assert result["id_schedule"] == "schedule-id-123"
        assert result["token"] == "fake_cancel_token"

        mock_repository.find_schedule_by_id.assert_called_once_with(mock_session, "schedule-id-123")
        mock_jwt_service_instance.create_token.assert_called_once_with({
            "sub": "schedule-id-123", 
            "role": ["request_cancel_schedule", "admin"]
        })


@pytest.mark.asyncio
async def test_request_cancel_schedule_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedule does not exist
    mock_repository.find_schedule_by_id.return_value = None

    use_case = RequestCancelScheduleUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError, match="Agendamento com o id schedule-id-nonexistent não encontrado"):
        await use_case.request_cancel(mock_session, "schedule-id-nonexistent")

    mock_repository.find_schedule_by_id.assert_called_once_with(mock_session, "schedule-id-nonexistent")


@pytest.mark.asyncio
async def test_request_cancel_schedule_with_different_id(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedule exists with different ID
    fake_schedule = MagicMock()
    fake_schedule.id = "schedule-id-456"
    mock_repository.find_schedule_by_id.return_value = fake_schedule

    # Mock JWT service
    with patch('src.modules.schedule.data.use_cases.request_cancel_schedule_use_case.JWTService') as mock_jwt_service_class:
        mock_jwt_service_instance = mock_jwt_service_class.return_value
        mock_jwt_service_instance.create_token.return_value = "another_cancel_token"

        use_case = RequestCancelScheduleUseCase(mock_repository)
        result = await use_case.request_cancel(mock_session, "schedule-id-456")

        assert result["id_schedule"] == "schedule-id-456"
        assert result["token"] == "another_cancel_token"

        mock_repository.find_schedule_by_id.assert_called_once_with(mock_session, "schedule-id-456")
        mock_jwt_service_instance.create_token.assert_called_once_with({
            "sub": "schedule-id-456", 
            "role": ["request_cancel_schedule", "admin"]
        })


@pytest.mark.asyncio 
async def test_format_response_method(mocker):
    # Test the private format response method directly
    use_case = RequestCancelScheduleUseCase(AsyncMock())
    
    result = use_case._RequestCancelScheduleUseCase__format_response("test-id", "test-token")
    
    assert result["id_schedule"] == "test-id"
    assert result["token"] == "test-token"
