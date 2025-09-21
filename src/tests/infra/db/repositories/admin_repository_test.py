import pytest
from unittest.mock import AsyncMock, MagicMock
from src.infra.db.entities.admin import Admin
from src.infra.db.repositories.admin_repository import AdminRepository

@pytest.mark.asyncio
async def test_get_admin_by_user(mocker):
    fake_user = "admin_user"
    fake_admin = Admin(user=fake_user)

    # Simula o retorno da query session.execute
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_admin

    # Simula uma instância da AsyncSession
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = AdminRepository(mock_session)
    admin = await repository.get_admin_by_user(fake_user)

    assert admin.user == fake_user
    mock_session.execute.assert_called_once()