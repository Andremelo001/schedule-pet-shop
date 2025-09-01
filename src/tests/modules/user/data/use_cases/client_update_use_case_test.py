import pytest
from unittest.mock import AsyncMock
from src.modules.user.data.use_cases.client_update_use_case import ClientUpdateUseCase
from src.modules.user.dto.client_dto import ClientUpdateDTO
from src.errors.types_errors import HttpNotFoundError, HttpConflitError, HttpBadRequestError
from src.infra.db.entities.client import Client

@pytest.mark.asyncio
async def test_update_client_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock no conflict with CPF
    mock_repository.get_client.return_value = None

    # Mock updated client
    updated_client = Client(
        id="client-id-123",
        name="Andre Updated",
        cpf="08855040383",
        age=26,
        email="andre.updated@gmail.com",
        senha="NewSenha123"
    )
    mock_repository.update_client.return_value = updated_client

    use_case = ClientUpdateUseCase(mock_repository)

    update_data = ClientUpdateDTO(
        name="Andre Updated",
        cpf="088.550.403-83",
        age=26,
        email="andre.updated@gmail.com",
        senha="NewSenha123"
    )

    result = await use_case.update(mock_session, "client-id-123", update_data)

    assert result["id"] == "client-id-123"
    assert result["name"] == "Andre Updated"
    assert result["cpf"] == "08855040383"
    assert result["age"] == 26
    assert result["email"] == "andre.updated@gmail.com"
    assert result["senha"] == "NewSenha123"

    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.get_client.assert_called_once_with(mock_session, "088.550.403-83")
    mock_repository.update_client.assert_called_once()

@pytest.mark.asyncio
async def test_update_client_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client does not exist
    mock_repository.get_client_by_id.return_value = None

    use_case = ClientUpdateUseCase(mock_repository)

    update_data = ClientUpdateDTO(name="Andre Updated")

    with pytest.raises(HttpNotFoundError) as exc_info:
        await use_case.update(mock_session, "client-id-123", update_data)

    assert "Cliente com o id client-id-123 não encontrado" in str(exc_info.value)
    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")

@pytest.mark.asyncio
async def test_update_client_cpf_conflict(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock another client with same CPF
    conflicting_client = Client(id="different-id")
    mock_repository.get_client.return_value = conflicting_client

    use_case = ClientUpdateUseCase(mock_repository)

    update_data = ClientUpdateDTO(cpf="08855040383")

    with pytest.raises(HttpConflitError) as exc_info:
        await use_case.update(mock_session, "client-id-123", update_data)

    assert "Cliente com o cpf 08855040383 já existe" in str(exc_info.value)

@pytest.mark.asyncio
async def test_update_client_invalid_email(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    use_case = ClientUpdateUseCase(mock_repository)

    update_data = ClientUpdateDTO(email="invalid-email")

    with pytest.raises(HttpBadRequestError):
        await use_case.update(mock_session, "client-id-123", update_data)

@pytest.mark.asyncio
async def test_update_client_invalid_senha(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    use_case = ClientUpdateUseCase(mock_repository)

    update_data = ClientUpdateDTO(senha="weak")

    with pytest.raises(HttpBadRequestError):
        await use_case.update(mock_session, "client-id-123", update_data)

@pytest.mark.asyncio
async def test_update_client_partial_update(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock updated client
    updated_client = Client(
        id="client-id-123",
        name="Andre Updated",
        cpf="original-cpf",
        age=25,
        email="original@gmail.com",
        senha="original-senha"
    )
    mock_repository.update_client.return_value = updated_client

    use_case = ClientUpdateUseCase(mock_repository)

    # Only update name
    update_data = ClientUpdateDTO(name="Andre Updated")

    result = await use_case.update(mock_session, "client-id-123", update_data)

    assert result["name"] == "Andre Updated"
    mock_repository.update_client.assert_called_once()

@pytest.mark.asyncio
async def test_update_client_same_cpf(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock same client with same CPF (should not conflict)
    same_client = Client(id="client-id-123")
    mock_repository.get_client.return_value = same_client

    # Mock updated client
    updated_client = Client(
        id="client-id-123",
        name="Andre",
        cpf="08855040383",
        age=25,
        email="andre@gmail.com",
        senha="senha123"
    )
    mock_repository.update_client.return_value = updated_client

    use_case = ClientUpdateUseCase(mock_repository)

    update_data = ClientUpdateDTO(cpf="08855040383")

    result = await use_case.update(mock_session, "client-id-123", update_data)

    assert result["cpf"] == "08855040383"
    mock_repository.update_client.assert_called_once()
