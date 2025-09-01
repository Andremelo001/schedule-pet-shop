import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.modules.authenticate_user.data.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from src.errors.types_errors.http_Unauthorized import HttpUnauthorized


@pytest.mark.asyncio
async def test_generate_token_user_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock user exists
    fake_user = MagicMock()
    fake_user.senha = "hashed_password"
    fake_user.email = "user@example.com"
    mock_repository.get_client_by_email.return_value = fake_user

    # Mock password verification success
    with patch('src.modules.authenticate_user.data.use_cases.authenticate_user_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance
        mock_password_hasher_instance.verify.return_value = True

        # Mock JWT service
        with patch('src.modules.authenticate_user.data.use_cases.authenticate_user_use_case.JWTService') as mock_jwt_service_class:
            mock_jwt_service_instance = MagicMock()
            mock_jwt_service_class.return_value = mock_jwt_service_instance
            mock_jwt_service_instance.create_token.return_value = "fake_jwt_token"

            use_case = AuthenticateUserUseCase(mock_repository)
            result = await use_case.generate_token(mock_session, "user@example.com", "correct_password")

            assert result == "fake_jwt_token"

            mock_repository.get_client_by_email.assert_called_once_with(mock_session, "user@example.com")
            mock_password_hasher_instance.verify.assert_called_once_with("correct_password", "hashed_password")
            mock_jwt_service_instance.create_token.assert_called_once_with({"sub": "correct_password", "role": "client"})


@pytest.mark.asyncio
async def test_generate_token_user_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock user does not exist
    mock_repository.get_client_by_email.return_value = None

    # Mock password verification
    with patch('src.modules.authenticate_user.data.use_cases.authenticate_user_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance

        use_case = AuthenticateUserUseCase(mock_repository)

        with pytest.raises(HttpUnauthorized, match="Invalid email or password"):
            await use_case.generate_token(mock_session, "nonexistent@example.com", "any_password")

        mock_repository.get_client_by_email.assert_called_once_with(mock_session, "nonexistent@example.com")


@pytest.mark.asyncio
async def test_generate_token_user_invalid_password(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock user exists
    fake_user = MagicMock()
    fake_user.senha = "hashed_password"
    fake_user.email = "user@example.com"
    mock_repository.get_client_by_email.return_value = fake_user

    # Mock password verification failure
    with patch('src.modules.authenticate_user.data.use_cases.authenticate_user_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance
        mock_password_hasher_instance.verify.return_value = False

        use_case = AuthenticateUserUseCase(mock_repository)

        with pytest.raises(HttpUnauthorized, match="Invalid email or password"):
            await use_case.generate_token(mock_session, "user@example.com", "wrong_password")

        mock_repository.get_client_by_email.assert_called_once_with(mock_session, "user@example.com")
        mock_password_hasher_instance.verify.assert_called_once_with("wrong_password", "hashed_password")


@pytest.mark.asyncio
async def test_verify_user_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock user exists
    fake_user = MagicMock()
    fake_user.senha = "hashed_password"
    fake_user.email = "user@example.com"
    mock_repository.get_client_by_email.return_value = fake_user

    # Mock password verification success
    with patch('src.modules.authenticate_user.data.use_cases.authenticate_user_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance
        mock_password_hasher_instance.verify.return_value = True

        use_case = AuthenticateUserUseCase(mock_repository)
        # Should not raise any exception
        await use_case.verify_user(mock_session, "user@example.com", "correct_password")

        mock_repository.get_client_by_email.assert_called_once_with(mock_session, "user@example.com")
        mock_password_hasher_instance.verify.assert_called_once_with("correct_password", "hashed_password")
