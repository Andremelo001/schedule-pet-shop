import pytest
from unittest.mock import AsyncMock, patch
from src.modules.user.data.use_cases.client_create_use_case import CreateClientUseCase
from src.modules.user.dto.client_dto import ClientDTO
from src.errors.types_errors import HttpBadRequestError, HttpConflitError

from src.infra.db.entities.client import Client

@pytest.mark.asyncio
async def test_create_client_success(mocker):

    mock_repository = AsyncMock()

    # Mock que não existe clientes cadastrados com o cpf
    mock_repository.get_client.return_value = None

    # Mock do PasswordHasher
    with patch('src.modules.user.data.use_cases.client_create_use_case.PasswordHasher') as mock_password_hasher:
        mock_hasher_instance = mock_password_hasher.return_value
        mock_hasher_instance.hash.return_value = "hashed_senha"

        # Mock do ClientFinderUseCase.validate_cpf
        with patch('src.modules.user.data.use_cases.client_create_use_case.ClientFinderUseCase.validate_cpf') as mock_validate_cpf:
            mock_validate_cpf.return_value = "123.456.789-09"

            use_case = CreateClientUseCase(mock_repository)

            client = ClientDTO(
                name="Andre",
                cpf="12345678909",
                age=20,
                email="andre@gmail.com",
                senha="Senha123"
            )

            result = await use_case.create( client)

            assert result == {"message": "Cliente cadastrado com sucesso"}

            # Verificar se o CPF foi usado para verificar existência (sem formatação)
            mock_repository.get_client.assert_called_once_with( "12345678909")
            
            # Verificar se o cliente foi criado no repositório
            mock_repository.create_client.assert_called_once_with( client)
            
            # Verificar se a senha foi criptografada
            mock_hasher_instance.hash.assert_called_once_with("Senha123")
            
            # Verificar se o CPF foi formatado
            mock_validate_cpf.assert_called_once_with("12345678909")

@pytest.mark.asyncio
async def test_client_already_exists(mocker):

    mock_repository = AsyncMock()

    # Mock que existe um cliente com esse CPF
    fake_client = Client(id="client-id-123")
    mock_repository.get_client.return_value = fake_client

    use_case = CreateClientUseCase(mock_repository)

    client = ClientDTO(
        name="Andre",
        cpf="12345678909",
        age=20,
        email="andre@gmail.com",
        senha="Senha123"
    )

    with pytest.raises(HttpConflitError, match="Cliente com o cpf 12345678909 já existe"):
        await use_case.create( client)

    # Verificar se foi chamado para verificar existência
    mock_repository.get_client.assert_called_once_with( "12345678909")

@pytest.mark.asyncio
async def test_invalid_email(mocker):

    mock_repository = AsyncMock()

    mock_repository.get_client.return_value = None

    use_case = CreateClientUseCase(mock_repository)

    client = ClientDTO(
        name="Andre",
        cpf="12345678909",
        age=20,
        email="andre.com",  # Email inválido (sem @)
        senha="Senha123"
    )

    with pytest.raises(HttpBadRequestError, match="O e-mail informado não é válido! Exemplo: ex@gmail.com"):
        await use_case.create( client)

    # Verificar se foi chamado para verificar existência antes da validação do email
    mock_repository.get_client.assert_called_once_with( "12345678909")

@pytest.mark.asyncio
async def test_invalid_senha(mocker):

    mock_repository = AsyncMock()

    mock_repository.get_client.return_value = None

    use_case = CreateClientUseCase(mock_repository)

    client = ClientDTO(
        name="Andre",
        cpf="12345678909",
        age=20,
        email="andre@gmail.com",
        senha="sammy"  # Senha inválida (sem maiúscula, sem número, menos de 8 caracteres)
    )

    with pytest.raises(HttpBadRequestError, match="A senha deve conter pelo menos uma letra maiúscula, um número e ter no mínimo 8 caracteres"):
        await use_case.create( client)

    # Verificar se foi chamado para verificar existência antes da validação da senha
    mock_repository.get_client.assert_called_once_with( "12345678909")


