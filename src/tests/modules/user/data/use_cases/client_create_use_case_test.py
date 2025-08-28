import pytest
from unittest.mock import AsyncMock
from src.modules.user.data.use_cases.client_create_use_case import CreateClientUseCase
from src.modules.user.dto.client_dto import ClientDTO
from src.errors.types_errors import HttpBadRequestError, HttpConflitError

from src.infra.db.entities.client import Client

@pytest.mark.asyncio
async def test_create_client_success(mocker):

    mock_repository = AsyncMock()

    mock_session = AsyncMock()

    #definir que não existe clientes cadastrados com o cpf
    mock_repository.get_client.return_value = None

    use_case = CreateClientUseCase(mock_repository)

    client = ClientDTO(
        name="Andre",
        cpf="08855040383",
        age=20,
        email="andre@gmail.com",
        senha="Senha123"
    )

    result = await use_case.create(mock_session, client)

    assert result == {"message": "Cliente cadastrado com sucesso"}

    mock_repository.get_client.assert_called_once()

@pytest.mark.asyncio
async def test_client_already_exists(mocker):

    mock_repository = AsyncMock()

    mock_session = AsyncMock()

    mock_repository.get_client.return_value = True

    use_case = CreateClientUseCase(mock_repository)

    client = ClientDTO(
        name="Andre",
        cpf="08855040383",
        age=20,
        email="andre@gmail.com",
        senha="Senha123"
    )

    with pytest.raises(HttpConflitError):
        await use_case.create(mock_session, client)

    mock_repository.get_client.assert_called_once()

@pytest.mark.asyncio
async def test_invalid_email(mocker):

    mock_repository = AsyncMock()

    mock_session = AsyncMock()

    mock_repository.get_client.return_value = None

    use_case = CreateClientUseCase(mock_repository)

    client = ClientDTO(
        name="Andre",
        cpf="08855040383",
        age=20,
        email="andre.com",
        senha="Senha123"
    )

    with pytest.raises(HttpBadRequestError):
        await use_case.create(mock_session, client)

    mock_repository.get_client.assert_called_once()

@pytest.mark.asyncio
async def test_invalid_senha(mocker):

    mock_repository = AsyncMock()

    mock_session = AsyncMock()

    mock_repository.get_client.return_value = None

    use_case = CreateClientUseCase(mock_repository)

    client = ClientDTO(
        name="Andre",
        cpf="08855040383",
        age=20,
        email="andre@gmail.com",
        senha="sammy"
    )

    with pytest.raises(HttpBadRequestError):
        await use_case.create(mock_session, client)

    mock_repository.get_client.assert_called_once()


