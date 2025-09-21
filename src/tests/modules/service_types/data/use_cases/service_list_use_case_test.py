import pytest
from unittest.mock import AsyncMock, MagicMock

from src.modules.service_types.data.use_cases.service_list_use_case import ServiceListUseCase


@pytest.mark.asyncio
async def test_list_services_success(mocker):
    mock_repository = AsyncMock()

    # Mock services exist
    mock_service_1 = MagicMock()
    mock_service_1.id = "service-id-1"
    mock_service_1.duration_in_minutes = 60
    mock_service_1.type_service = "banho"
    mock_service_1.price = 30.0

    mock_service_2 = MagicMock()
    mock_service_2.id = "service-id-2"
    mock_service_2.duration_in_minutes = 45
    mock_service_2.type_service = "tosa"
    mock_service_2.price = 50.0

    mock_repository.list_services.return_value = [mock_service_1, mock_service_2]

    use_case = ServiceListUseCase(mock_repository)
    result = await use_case.list()

    assert len(result) == 2
    
    # Check first service
    assert result[0]["id"] == "service-id-1"
    assert result[0]["duration_in_minutes"] == 60
    assert result[0]["type_service"] == "banho"
    assert result[0]["price"] == 30.0

    # Check second service
    assert result[1]["id"] == "service-id-2"
    assert result[1]["duration_in_minutes"] == 45
    assert result[1]["type_service"] == "tosa"
    assert result[1]["price"] == 50.0

    mock_repository.list_services.assert_called_once_with()


@pytest.mark.asyncio
async def test_list_services_empty(mocker):
    mock_repository = AsyncMock()

    # Mock no services
    mock_repository.list_services.return_value = []

    use_case = ServiceListUseCase(mock_repository)
    result = await use_case.list()

    assert len(result) == 0
    assert result == []

    mock_repository.list_services.assert_called_once_with()


@pytest.mark.asyncio
async def test_list_services_single_service(mocker):
    mock_repository = AsyncMock()

    # Mock single service
    mock_service = MagicMock()
    mock_service.id = "service-id-1"
    mock_service.duration_in_minutes = 30
    mock_service.type_service = "secar"
    mock_service.price = 20.0

    mock_repository.list_services.return_value = [mock_service]

    use_case = ServiceListUseCase(mock_repository)
    result = await use_case.list()

    assert len(result) == 1
    assert result[0]["id"] == "service-id-1"
    assert result[0]["duration_in_minutes"] == 30
    assert result[0]["type_service"] == "secar"
    assert result[0]["price"] == 20.0

    mock_repository.list_services.assert_called_once_with()
