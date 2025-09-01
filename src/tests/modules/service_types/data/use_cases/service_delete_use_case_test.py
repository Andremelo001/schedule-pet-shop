import pytest
from unittest.mock import AsyncMock, MagicMock

from src.modules.service_types.data.use_cases.service_delete_use_case import ServiceDeleteUseCase
from src.errors.types_errors.http_not_found import HttpNotFoundError
from src.errors.types_errors.http_Unauthorized import HttpUnauthorized


@pytest.mark.asyncio
async def test_delete_service_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock service exists
    fake_service = MagicMock()
    fake_service.id = "service-id-123"
    mock_repository.find_service_by_id.return_value = fake_service

    # Mock no schedules using this service
    mock_repository.get_schedules_by_service_id.return_value = []

    use_case = ServiceDeleteUseCase(mock_repository)
    result = await use_case.delete(mock_session, "service-id-123")

    assert result["message"] == "Serviço deletado com sucesso"

    mock_repository.find_service_by_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.get_schedules_by_service_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.delete_service.assert_called_once_with(mock_session, "service-id-123")


@pytest.mark.asyncio
async def test_delete_service_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock service does not exist
    mock_repository.find_service_by_id.return_value = None

    use_case = ServiceDeleteUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError, match="Serviço com o id service-id-nonexistent não encontrado"):
        await use_case.delete(mock_session, "service-id-nonexistent")

    mock_repository.find_service_by_id.assert_called_once_with(mock_session, "service-id-nonexistent")


@pytest.mark.asyncio
async def test_delete_service_with_active_schedules(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock service exists
    fake_service = MagicMock()
    fake_service.id = "service-id-123"
    mock_repository.find_service_by_id.return_value = fake_service

    # Mock schedules using this service
    fake_schedule = MagicMock()
    fake_schedule.id = "schedule-id-123"
    mock_repository.get_schedules_by_service_id.return_value = [fake_schedule]

    use_case = ServiceDeleteUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Serviço não pode ser deletado, pois à agendamentos cadastrados com esse serviço!"):
        await use_case.delete(mock_session, "service-id-123")

    mock_repository.find_service_by_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.get_schedules_by_service_id.assert_called_once_with(mock_session, "service-id-123")


@pytest.mark.asyncio
async def test_delete_service_with_empty_schedules(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock service exists
    fake_service = MagicMock()
    fake_service.id = "service-id-123"
    mock_repository.find_service_by_id.return_value = fake_service

    # Mock schedules list with None values (empty schedules)
    mock_repository.get_schedules_by_service_id.return_value = [None, None]

    use_case = ServiceDeleteUseCase(mock_repository)
    result = await use_case.delete(mock_session, "service-id-123")

    assert result["message"] == "Serviço deletado com sucesso"

    mock_repository.find_service_by_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.get_schedules_by_service_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.delete_service.assert_called_once_with(mock_session, "service-id-123")
