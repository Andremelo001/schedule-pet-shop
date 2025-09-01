import pytest
from unittest.mock import AsyncMock
from src.modules.user.data.use_cases.client_finder_use_case import ClientFinderUseCase
from src.errors.types_errors import HttpNotFoundError, HttpBadRequestError
from src.infra.db.entities.client import Client

@pytest.mark.asyncio
async def test_find_client_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(
        id="client-id-123",
        name="Andre",
        age=25,
        email="andre@gmail.com",
        senha="senha123"
    )
    mock_repository.get_client.return_value = fake_client

    use_case = ClientFinderUseCase(mock_repository)

    result = await use_case.find(mock_session, "08855040383")

    assert result["id"] == "client-id-123"
    assert result["name"] == "Andre"
    assert result["age"] == 25
    assert result["email"] == "andre@gmail.com"
    assert result["senha"] == "senha123"
    mock_repository.get_client.assert_called_once_with(mock_session, "08855040383")

@pytest.mark.asyncio
async def test_find_client_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client does not exist
    mock_repository.get_client.return_value = None

    use_case = ClientFinderUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError) as exc_info:
        await use_case.find(mock_session, "08855040383")

    assert "Nenhum cliente encontrado com o cpf 08855040383" in str(exc_info.value)
    mock_repository.get_client.assert_called_once_with(mock_session, "08855040383")

@pytest.mark.asyncio
async def test_find_client_invalid_cpf_length(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    use_case = ClientFinderUseCase(mock_repository)

    with pytest.raises(HttpBadRequestError) as exc_info:
        await use_case.find(mock_session, "123456789")  # 9 digits

    assert "Cpf informado não apresenta 11 dígitos" in str(exc_info.value)

@pytest.mark.asyncio
async def test_find_client_cpf_all_same_digits(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    use_case = ClientFinderUseCase(mock_repository)

    with pytest.raises(HttpBadRequestError) as exc_info:
        await use_case.find(mock_session, "11111111111")  # All same digits

    assert "Cpf informado apresenta todos os dígitos iguais" in str(exc_info.value)

@pytest.mark.asyncio
async def test_find_client_invalid_cpf_digits(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    use_case = ClientFinderUseCase(mock_repository)

    with pytest.raises(HttpBadRequestError) as exc_info:
        await use_case.find(mock_session, "12345678900")  # Invalid CPF

    assert "Cpf informado é inválido" in str(exc_info.value)

@pytest.mark.asyncio
async def test_find_client_cpf_with_formatting(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(
        id="client-id-123",
        name="Andre",
        age=25,
        email="andre@gmail.com",
        senha="senha123"
    )
    mock_repository.get_client.return_value = fake_client

    use_case = ClientFinderUseCase(mock_repository)

    # Test with formatted CPF
    result = await use_case.find(mock_session, "088.550.403-83")

    assert result["name"] == "Andre"
    # Should call with clean CPF (no formatting)
    mock_repository.get_client.assert_called_once_with(mock_session, "08855040383")
