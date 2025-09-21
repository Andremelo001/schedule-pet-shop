import pytest
from unittest.mock import AsyncMock
from src.modules.pet.data.use_cases.pet_delete_use_case import PetDeleteUseCase
from src.errors.types_errors import HttpNotFoundError
from src.infra.db.entities.pet import Pet

@pytest.mark.asyncio
async def test_delete_pet_success(mocker):
    mock_repository = AsyncMock()

    # Mock pet exists
    fake_pet = Pet(id="pet-id-123")
    mock_repository.get_pet.return_value = fake_pet

    use_case = PetDeleteUseCase(mock_repository)

    result = await use_case.delete( "pet-id-123")

    assert result == {"message": "Pet deletado com sucesso do banco de dados"}
    mock_repository.get_pet.assert_called_once_with( "pet-id-123")
    mock_repository.delete_pet.assert_called_once_with( "pet-id-123")

@pytest.mark.asyncio
async def test_delete_pet_not_found(mocker):
    mock_repository = AsyncMock()

    # Mock pet does not exist
    mock_repository.get_pet.return_value = None

    use_case = PetDeleteUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError) as exc_info:
        await use_case.delete( "pet-id-123")

    assert "Pet com o id pet-id-123 não encontrado" in str(exc_info.value)
    mock_repository.get_pet.assert_called_once_with( "pet-id-123")
