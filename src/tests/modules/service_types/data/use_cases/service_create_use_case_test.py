import pytest
from unittest.mock import AsyncMock, MagicMock

from src.modules.service_types.data.use_cases.service_create_use_case import ServiceCreateUseCase
from src.errors.types_errors.http_Unauthorized import HttpUnauthorized


@pytest.mark.asyncio
async def test_create_service_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock no existing services
    mock_repository.list_services.return_value = []

    use_case = ServiceCreateUseCase(mock_repository)

    # Use MagicMock for service_data
    service_data = MagicMock()
    service_data.duration_in_minutes = 60
    service_data.type_service = "banho"
    service_data.price = 30.0

    result = await use_case.create(mock_session, service_data)

    assert result["message"] == "Serviço cadastrado com sucesso"

    mock_repository.list_services.assert_called_once_with(mock_session)
    mock_repository.create_service.assert_called_once_with(mock_session, service_data)


@pytest.mark.asyncio
async def test_create_service_invalid_type(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    use_case = ServiceCreateUseCase(mock_repository)

    # Use MagicMock for service_data with invalid type
    service_data = MagicMock()
    service_data.duration_in_minutes = 60
    service_data.type_service = "invalid_service"
    service_data.price = 30.0

    with pytest.raises(HttpUnauthorized, match="Tipo de serviço não aceito, escolha um dos serviços disponíveis: banho, secar, tosa"):
        await use_case.create(mock_session, service_data)


@pytest.mark.asyncio
async def test_create_service_already_exists(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock existing service with same type and price
    existing_service = MagicMock()
    existing_service.type_service = "banho"
    existing_service.price = 30.0

    mock_repository.list_services.return_value = [existing_service]

    use_case = ServiceCreateUseCase(mock_repository)

    # Use MagicMock for service_data with same type and price
    service_data = MagicMock()
    service_data.duration_in_minutes = 60
    service_data.type_service = "banho"
    service_data.price = 30.0

    with pytest.raises(HttpUnauthorized, match="Serviço já existe no banco de dados"):
        await use_case.create(mock_session, service_data)

    mock_repository.list_services.assert_called_once_with(mock_session)


@pytest.mark.asyncio
async def test_create_service_different_price_same_type(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock existing service with same type but different price
    existing_service = MagicMock()
    existing_service.type_service = "banho"
    existing_service.price = 25.0

    mock_repository.list_services.return_value = [existing_service]

    use_case = ServiceCreateUseCase(mock_repository)

    # Use MagicMock for service_data with same type but different price
    service_data = MagicMock()
    service_data.duration_in_minutes = 60
    service_data.type_service = "banho"
    service_data.price = 30.0

    result = await use_case.create(mock_session, service_data)

    assert result["message"] == "Serviço cadastrado com sucesso"

    mock_repository.list_services.assert_called_once_with(mock_session)
    mock_repository.create_service.assert_called_once_with(mock_session, service_data)
