import pytest
from unittest.mock import AsyncMock, MagicMock
from src.modules.user.data.use_cases.client_delete_use_case import ClientDeleteUseCase
from src.errors.types_errors import HttpNotFoundError, HttpUnauthorized
from src.infra.db.entities.client import Client

@pytest.mark.asyncio
async def test_delete_client_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock no active schedules
    mock_repository.find_schedule_by_id_client.return_value = []

    use_case = ClientDeleteUseCase(mock_repository)

    result = await use_case.delete(mock_session, "client-id-123")

    assert result == {"message": "Cliente deletado com sucesso do banco de dados"}
    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.find_schedule_by_id_client.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.delete_client.assert_called_once_with(mock_session, "client-id-123")

@pytest.mark.asyncio
async def test_delete_client_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client does not exist
    mock_repository.get_client_by_id.return_value = None

    use_case = ClientDeleteUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError) as exc_info:
        await use_case.delete(mock_session, "client-id-123")

    assert "Cliente com o id client-id-123 não encontrado" in str(exc_info.value)
    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")

@pytest.mark.asyncio
async def test_delete_client_with_active_schedules(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock active schedules
    mock_schedule_active = MagicMock()
    mock_schedule_active.schedule_active = True
    mock_repository.find_schedule_by_id_client.return_value = [mock_schedule_active]

    use_case = ClientDeleteUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized) as exc_info:
        await use_case.delete(mock_session, "client-id-123")

    assert "Não é possivel deletar o cliente, pois ele apresenta agendamentos ativos" in str(exc_info.value)
    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.find_schedule_by_id_client.assert_called_once_with(mock_session, "client-id-123")

@pytest.mark.asyncio
async def test_delete_client_with_inactive_schedules(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock inactive schedules only
    mock_schedule_inactive = MagicMock()
    mock_schedule_inactive.schedule_active = False
    mock_repository.find_schedule_by_id_client.return_value = [mock_schedule_inactive]

    use_case = ClientDeleteUseCase(mock_repository)

    result = await use_case.delete(mock_session, "client-id-123")

    assert result == {"message": "Cliente deletado com sucesso do banco de dados"}
    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.find_schedule_by_id_client.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.delete_client.assert_called_once_with(mock_session, "client-id-123")
