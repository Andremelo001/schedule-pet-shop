import pytest
from unittest.mock import AsyncMock, MagicMock

from src.modules.service_types.data.use_cases.service_update_use_case import ServiceUpdateUseCase
from src.errors.types_errors.http_not_found import HttpNotFoundError
from src.errors.types_errors.http_Unauthorized import HttpUnauthorized


@pytest.mark.asyncio
async def test_update_service_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock service exists
    fake_service = MagicMock()
    fake_service.id = "service-id-123"
    mock_repository.find_service_by_id.return_value = fake_service

    # Mock no schedules using this service
    mock_repository.get_schedules_by_service_id.return_value = []

    # Mock updated service
    updated_service = MagicMock()
    updated_service.id = "service-id-123"
    updated_service.duration_in_minutes = 90
    updated_service.type_service = "banho"
    updated_service.price = 35.0

    mock_repository.update_service.return_value = updated_service

    use_case = ServiceUpdateUseCase(mock_repository)

    # Use MagicMock for update_data
    update_data = MagicMock()
    update_data.duration_in_minutes = 90
    update_data.type_service = "banho"
    update_data.price = 35.0

    result = await use_case.update(mock_session, update_data, "service-id-123")

    assert result["id"] == "service-id-123"
    assert result["duration_in_minutes"] == 90
    assert result["type_service"] == "banho"
    assert result["price"] == 35.0

    mock_repository.get_schedules_by_service_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.find_service_by_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.update_service.assert_called_once_with(mock_session, update_data, "service-id-123")


@pytest.mark.asyncio
async def test_update_service_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock no schedules using this service
    mock_repository.get_schedules_by_service_id.return_value = []

    # Mock service does not exist
    mock_repository.find_service_by_id.return_value = None

    use_case = ServiceUpdateUseCase(mock_repository)

    # Use MagicMock for update_data
    update_data = MagicMock()
    update_data.duration_in_minutes = 90
    update_data.type_service = None
    update_data.price = 35.0

    with pytest.raises(HttpNotFoundError, match="Serviço não encontrado em nossa base de dados"):
        await use_case.update(mock_session, update_data, "service-id-nonexistent")

    mock_repository.get_schedules_by_service_id.assert_called_once_with(mock_session, "service-id-nonexistent")
    mock_repository.find_service_by_id.assert_called_once_with(mock_session, "service-id-nonexistent")


@pytest.mark.asyncio
async def test_update_service_invalid_type(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    use_case = ServiceUpdateUseCase(mock_repository)

    # Use MagicMock for update_data with invalid type
    update_data = MagicMock()
    update_data.duration_in_minutes = 90
    update_data.type_service = "invalid_service"
    update_data.price = 35.0

    with pytest.raises(HttpUnauthorized, match="Tipo de serviço não aceito, escolha um dos serviços disponíveis: banho, secar, tosa"):
        await use_case.update(mock_session, update_data, "service-id-123")


@pytest.mark.asyncio
async def test_update_service_with_active_schedules(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock schedules using this service
    fake_schedule = MagicMock()
    fake_schedule.id = "schedule-id-123"
    mock_repository.get_schedules_by_service_id.return_value = [fake_schedule]

    use_case = ServiceUpdateUseCase(mock_repository)

    # Use MagicMock for update_data
    update_data = MagicMock()
    update_data.duration_in_minutes = 90
    update_data.type_service = None
    update_data.price = 35.0

    with pytest.raises(HttpUnauthorized, match="Não é possivel atualizar o serviço com id service-id-123, pois existe um agendamento com esse serviço"):
        await use_case.update(mock_session, update_data, "service-id-123")

    mock_repository.get_schedules_by_service_id.assert_called_once_with(mock_session, "service-id-123")


@pytest.mark.asyncio
async def test_update_service_partial_update(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock service exists
    fake_service = MagicMock()
    fake_service.id = "service-id-123"
    mock_repository.find_service_by_id.return_value = fake_service

    # Mock no schedules using this service
    mock_repository.get_schedules_by_service_id.return_value = []

    # Mock updated service with partial data
    updated_service = MagicMock()
    updated_service.id = "service-id-123"
    updated_service.duration_in_minutes = 60
    updated_service.type_service = "banho"
    updated_service.price = 40.0

    mock_repository.update_service.return_value = updated_service

    use_case = ServiceUpdateUseCase(mock_repository)

    # Only update price
    update_data = MagicMock()
    update_data.duration_in_minutes = None
    update_data.type_service = None
    update_data.price = 40.0

    result = await use_case.update(mock_session, update_data, "service-id-123")

    assert result["id"] == "service-id-123"
    assert result["duration_in_minutes"] == 60
    assert result["type_service"] == "banho"
    assert result["price"] == 40.0

    mock_repository.get_schedules_by_service_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.find_service_by_id.assert_called_once_with(mock_session, "service-id-123")
    mock_repository.update_service.assert_called_once_with(mock_session, update_data, "service-id-123")
