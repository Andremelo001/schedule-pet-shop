import pytest
from unittest.mock import AsyncMock, MagicMock

from src.modules.pet.data.use_cases.get_all_pets_by_cpf_client_use_case import GetAllPetsByCpfClientUseCase
from src.errors.types_errors.http_not_found import HttpNotFoundError


@pytest.mark.asyncio
async def test_get_all_pets_by_cpf_client_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock pets exist
    mock_pet_1 = MagicMock()
    mock_pet_1.id = "pet-id-1"
    mock_pet_1.name = "Rex"
    mock_pet_1.breed = "Golden Retriever"
    mock_pet_1.age = 3
    mock_pet_1.size_in_centimeters = 60
    mock_pet_1.client_id = "client-id-123"

    mock_pet_2 = MagicMock()
    mock_pet_2.id = "pet-id-2"
    mock_pet_2.name = "Luna"
    mock_pet_2.breed = "Labrador"
    mock_pet_2.age = 2
    mock_pet_2.size_in_centimeters = 55
    mock_pet_2.client_id = "client-id-123"

    mock_repository.get_all_pets_by_cpf_client.return_value = [mock_pet_1, mock_pet_2]

    use_case = GetAllPetsByCpfClientUseCase(mock_repository)
    result = await use_case.get_all_pets(mock_session, "08855040383")

    assert len(result) == 2
    
    # Check first pet
    assert result[0]["id"] == "pet-id-1"
    assert result[0]["name"] == "Rex"
    assert result[0]["breed"] == "Golden Retriever"
    assert result[0]["age"] == 3
    assert result[0]["size_in_centimeters"] == 60
    assert result[0]["client_id"] == "client-id-123"

    # Check second pet
    assert result[1]["id"] == "pet-id-2"
    assert result[1]["name"] == "Luna"
    assert result[1]["breed"] == "Labrador"
    assert result[1]["age"] == 2
    assert result[1]["size_in_centimeters"] == 55
    assert result[1]["client_id"] == "client-id-123"

    mock_repository.get_all_pets_by_cpf_client.assert_called_once_with(mock_session, "08855040383")


@pytest.mark.asyncio
async def test_get_all_pets_by_cpf_client_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock no pets found
    mock_repository.get_all_pets_by_cpf_client.return_value = []

    use_case = GetAllPetsByCpfClientUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError, match="Pets do cliente não encontrados"):
        await use_case.get_all_pets(mock_session, "08855040383")

    mock_repository.get_all_pets_by_cpf_client.assert_called_once_with(mock_session, "08855040383")


@pytest.mark.asyncio
async def test_get_all_pets_by_cpf_client_single_pet(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock single pet
    mock_pet = MagicMock()
    mock_pet.id = "pet-id-1"
    mock_pet.name = "Rex"
    mock_pet.breed = "Golden Retriever"
    mock_pet.age = 3
    mock_pet.size_in_centimeters = 60
    mock_pet.client_id = "client-id-123"

    mock_repository.get_all_pets_by_cpf_client.return_value = [mock_pet]

    use_case = GetAllPetsByCpfClientUseCase(mock_repository)
    result = await use_case.get_all_pets(mock_session, "08855040383")

    assert len(result) == 1
    assert result[0]["id"] == "pet-id-1"
    assert result[0]["name"] == "Rex"
    assert result[0]["breed"] == "Golden Retriever"
    assert result[0]["age"] == 3
    assert result[0]["size_in_centimeters"] == 60
    assert result[0]["client_id"] == "client-id-123"

    mock_repository.get_all_pets_by_cpf_client.assert_called_once_with(mock_session, "08855040383")
