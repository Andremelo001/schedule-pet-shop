import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.modules.authenticate_admin.data.use_cases.authenticate_admin_use_case import AutheticateAdminUseCase
from src.errors.types_errors.http_Unauthorized import HttpUnauthorized


@pytest.mark.asyncio
async def test_generate_token_admin_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock admin exists
    fake_admin = MagicMock()
    fake_admin.senha = "hashed_password"
    fake_admin.user = "admin_user"
    mock_repository.get_admin_by_user.return_value = fake_admin

    # Mock password verification success
    with patch('src.modules.authenticate_admin.data.use_cases.authenticate_admin_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance
        mock_password_hasher_instance.verify.return_value = True

        # Mock JWT service
        with patch('src.modules.authenticate_admin.data.use_cases.authenticate_admin_use_case.JWTService') as mock_jwt_service_class:
            mock_jwt_service_instance = MagicMock()
            mock_jwt_service_class.return_value = mock_jwt_service_instance
            mock_jwt_service_instance.create_token.return_value = "fake_jwt_token"

            use_case = AutheticateAdminUseCase(mock_repository)
            result = await use_case.generate_token_admin(mock_session, "correct_password", "admin_user")

            assert result == "fake_jwt_token"

            mock_repository.get_admin_by_user.assert_called_once_with(mock_session, "admin_user")
            mock_password_hasher_instance.verify.assert_called_once_with("correct_password", "hashed_password")
            mock_jwt_service_instance.create_token.assert_called_once_with({"sub": "correct_password", "role": "admin"})


@pytest.mark.asyncio
async def test_generate_token_admin_user_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock admin does not exist
    mock_repository.get_admin_by_user.return_value = None

    # Mock password verification
    with patch('src.modules.authenticate_admin.data.use_cases.authenticate_admin_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance

        use_case = AutheticateAdminUseCase(mock_repository)

        with pytest.raises(HttpUnauthorized, match="Invalid email or password"):
            await use_case.generate_token_admin(mock_session, "any_password", "nonexistent_user")

        mock_repository.get_admin_by_user.assert_called_once_with(mock_session, "nonexistent_user")


@pytest.mark.asyncio
async def test_generate_token_admin_invalid_password(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock admin exists
    fake_admin = MagicMock()
    fake_admin.senha = "hashed_password"
    fake_admin.user = "admin_user"
    mock_repository.get_admin_by_user.return_value = fake_admin

    # Mock password verification failure
    with patch('src.modules.authenticate_admin.data.use_cases.authenticate_admin_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance
        mock_password_hasher_instance.verify.return_value = False

        use_case = AutheticateAdminUseCase(mock_repository)

        with pytest.raises(HttpUnauthorized, match="Invalid email or password"):
            await use_case.generate_token_admin(mock_session, "wrong_password", "admin_user")

        mock_repository.get_admin_by_user.assert_called_once_with(mock_session, "admin_user")
        mock_password_hasher_instance.verify.assert_called_once_with("wrong_password", "hashed_password")


@pytest.mark.asyncio
async def test_verify_user_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock admin exists
    fake_admin = MagicMock()
    fake_admin.senha = "hashed_password"
    fake_admin.user = "admin_user"
    mock_repository.get_admin_by_user.return_value = fake_admin

    # Mock password verification success
    with patch('src.modules.authenticate_admin.data.use_cases.authenticate_admin_use_case.PasswordHasher') as mock_password_hasher_class:
        mock_password_hasher_instance = MagicMock()
        mock_password_hasher_class.return_value = mock_password_hasher_instance
        mock_password_hasher_instance.verify.return_value = True

        use_case = AutheticateAdminUseCase(mock_repository)
        # Should not raise any exception
        await use_case.verify_user(mock_session, "correct_password", "admin_user")

        mock_repository.get_admin_by_user.assert_called_once_with(mock_session, "admin_user")
        mock_password_hasher_instance.verify.assert_called_once_with("correct_password", "hashed_password")
