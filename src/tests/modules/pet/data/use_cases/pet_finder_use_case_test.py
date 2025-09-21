import pytest
from unittest.mock import AsyncMock, MagicMock

from src.modules.pet.data.use_cases.pet_finder_use_case import PetFinderUseCase
from src.errors.types_errors.http_not_found import HttpNotFoundError


@pytest.mark.asyncio
async def test_find_pet_success(mocker):
    mock_repository = AsyncMock()

    # Mock pet exists
    fake_pet = MagicMock()
    fake_pet.id = "pet-id-123"
    fake_pet.name = "Rex"
    fake_pet.breed = "Golden Retriever"
    fake_pet.age = 3
    fake_pet.size_in_centimeters = 60
    fake_pet.client_id = "client-id-123"

    mock_repository.get_pet.return_value = fake_pet

    use_case = PetFinderUseCase(mock_repository)
    result = await use_case.finder( "pet-id-123")

    assert result["id"] == "pet-id-123"
    assert result["name"] == "Rex"
    assert result["breed"] == "Golden Retriever"
    assert result["age"] == 3
    assert result["size_in_centimeters"] == 60
    assert result["client_id"] == "client-id-123"

    mock_repository.get_pet.assert_called_once_with( "pet-id-123")


@pytest.mark.asyncio
async def test_find_pet_not_found(mocker):
    mock_repository = AsyncMock()

    # Mock pet does not exist
    mock_repository.get_pet.return_value = None

    use_case = PetFinderUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError, match="Pet com o id pet-id-nonexistent não encontrado"):
        await use_case.finder( "pet-id-nonexistent")

    mock_repository.get_pet.assert_called_once_with( "pet-id-nonexistent")
