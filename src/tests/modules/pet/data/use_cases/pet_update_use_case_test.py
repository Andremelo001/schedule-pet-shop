import pytest
from unittest.mock import AsyncMock, MagicMock

from src.modules.pet.data.use_cases.pet_update_use_case import PetUpdateUseCase
from src.modules.pet.dto.pet_dto import PetUpdateDTO
from src.errors.types_errors.http_conflit import HttpConflitError


@pytest.mark.asyncio
async def test_update_pet_success(mocker):
    mock_repository = AsyncMock()

    # Mock no conflicting pet names
    mock_repository.get_name_pet_by_id_client.return_value = ["Luna", "Max"]

    # Mock updated pet
    updated_pet = MagicMock()
    updated_pet.id = "pet-id-123"
    updated_pet.name = "Rex Updated"
    updated_pet.breed = "Golden Retriever Updated"
    updated_pet.age = 4
    updated_pet.size_in_centimeters = 65
    updated_pet.client_id = "client-id-123"

    mock_repository.uptdate_pet.return_value = updated_pet

    use_case = PetUpdateUseCase(mock_repository)

    update_data = PetUpdateDTO(
        name="Rex Updated",
        breed="Golden Retriever Updated", 
        age=4,
        size_in_centimeters="65"
    )

    result = await use_case.update( "client-id-123", "pet-id-123", update_data)

    assert result["id"] == "pet-id-123"
    assert result["name"] == "Rex Updated"
    assert result["breed"] == "Golden Retriever Updated"
    assert result["age"] == 4
    assert result["size_in_centimeters"] == 65
    assert result["client_id"] == "client-id-123"

    mock_repository.get_name_pet_by_id_client.assert_called_once_with( "client-id-123")
    mock_repository.uptdate_pet.assert_called_once_with( "pet-id-123", update_data)


@pytest.mark.asyncio
async def test_update_pet_name_conflict(mocker):
    mock_repository = AsyncMock()

    # Mock conflicting pet names
    mock_repository.get_name_pet_by_id_client.return_value = ["Rex", "Luna", "Max"]

    use_case = PetUpdateUseCase(mock_repository)

    update_data = PetUpdateDTO(
        name="Rex",
        breed="Golden Retriever Updated"
    )

    with pytest.raises(HttpConflitError, match="Pet com o nome Rex já existe"):
        await use_case.update( "client-id-123", "pet-id-123", update_data)

    mock_repository.get_name_pet_by_id_client.assert_called_once_with( "client-id-123")


@pytest.mark.asyncio
async def test_update_pet_partial_update(mocker):
    mock_repository = AsyncMock()

    # Mock no conflicting pet names
    mock_repository.get_name_pet_by_id_client.return_value = ["Luna", "Max"]

    # Mock updated pet with partial data
    updated_pet = MagicMock()
    updated_pet.id = "pet-id-123"
    updated_pet.name = "Rex"
    updated_pet.breed = "Golden Retriever"
    updated_pet.age = 4
    updated_pet.size_in_centimeters = 60
    updated_pet.client_id = "client-id-123"

    mock_repository.uptdate_pet.return_value = updated_pet

    use_case = PetUpdateUseCase(mock_repository)

    # Only update age
    update_data = PetUpdateDTO(age=4)

    result = await use_case.update( "client-id-123", "pet-id-123", update_data)

    assert result["id"] == "pet-id-123"
    assert result["name"] == "Rex"
    assert result["breed"] == "Golden Retriever"
    assert result["age"] == 4
    assert result["size_in_centimeters"] == 60
    assert result["client_id"] == "client-id-123"

    mock_repository.get_name_pet_by_id_client.assert_called_once_with( "client-id-123")
    mock_repository.uptdate_pet.assert_called_once_with( "pet-id-123", update_data)
