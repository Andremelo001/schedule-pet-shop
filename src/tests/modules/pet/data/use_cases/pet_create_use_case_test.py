import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import uuid

from src.modules.pet.data.use_cases.pet_create_use_case import PetCreateUseCase
from src.errors.types_errors import HttpNotFoundError, HttpConflitError
from src.infra.db.entities.client import Client

@pytest.mark.asyncio
async def test_create_pet_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id=str(uuid.uuid4()))

    # Mock pet names (no conflict)
    mock_repository.get_name_pet_by_id_client.return_value = ["Other Pet Name"]

    # Mock created pet
    created_pet = MagicMock()
    created_pet.id = str(uuid.uuid4())
    created_pet.name = "Rex"
    created_pet.breed = "Golden Retriever"
    created_pet.age = 3
    created_pet.size_in_centimeters = 60
    created_pet.client_id = fake_client.id

    mock_repository.create_pet.return_value = created_pet

    with patch('src.modules.pet.data.use_cases.pet_create_use_case.ClientRepository') as mock_client_repo_class:
        mock_client_repo_instance = AsyncMock()
        mock_client_repo_class.return_value = mock_client_repo_instance
        mock_client_repo_instance.get_client_by_id.return_value = fake_client

        use_case = PetCreateUseCase(mock_repository)

        # Use MagicMock for pet_data instead of PetDTO
        pet_data = MagicMock()
        pet_data.id_client = fake_client.id
        pet_data.name = "Rex"
        pet_data.breed = "Golden Retriever"
        pet_data.age = 3
        pet_data.size_in_centimeters = 60

        result = await use_case.create(mock_session, pet_data, fake_client.id)

        assert result["message"] == "Pet cadastrado com sucesso"

        mock_client_repo_instance.get_client_by_id.assert_called_once_with(mock_session, fake_client.id)
        mock_repository.get_name_pet_by_id_client.assert_called_once_with(mock_session, fake_client.id)
        mock_repository.create_pet.assert_called_once_with(mock_session, fake_client.id, pet_data)


@pytest.mark.asyncio
async def test_create_pet_client_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    client_id = str(uuid.uuid4())

    with patch('src.modules.pet.data.use_cases.pet_create_use_case.ClientRepository') as mock_client_repo_class:
        mock_client_repo_instance = AsyncMock()
        mock_client_repo_class.return_value = mock_client_repo_instance
        mock_client_repo_instance.get_client_by_id.return_value = None

        use_case = PetCreateUseCase(mock_repository)

        # Use MagicMock for pet_data instead of PetDTO
        pet_data = MagicMock()
        pet_data.id_client = client_id
        pet_data.name = "Rex"
        pet_data.breed = "Golden Retriever"
        pet_data.age = 3
        pet_data.size_in_centimeters = 60

        with pytest.raises(HttpNotFoundError, match=f"Cliente com o id {client_id} não encontrado"):
            await use_case.create(mock_session, pet_data, client_id)

        mock_client_repo_instance.get_client_by_id.assert_called_once_with(mock_session, client_id)


@pytest.mark.asyncio
async def test_create_pet_name_conflict(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id=str(uuid.uuid4()))

    # Mock pet names (with conflict)
    mock_repository.get_name_pet_by_id_client.return_value = ["Rex", "Luna"]

    with patch('src.modules.pet.data.use_cases.pet_create_use_case.ClientRepository') as mock_client_repo_class:
        mock_client_repo_instance = AsyncMock()
        mock_client_repo_class.return_value = mock_client_repo_instance
        mock_client_repo_instance.get_client_by_id.return_value = fake_client

        use_case = PetCreateUseCase(mock_repository)

        # Use MagicMock for pet_data instead of PetDTO
        pet_data = MagicMock()
        pet_data.id_client = fake_client.id
        pet_data.name = "Rex"  # Same name as existing pet
        pet_data.breed = "Golden Retriever"
        pet_data.age = 3
        pet_data.size_in_centimeters = 60

        with pytest.raises(HttpConflitError, match=f"Cliente com o id {fake_client.id}, já tem um pet cadastrado com o nome Rex"):
            await use_case.create(mock_session, pet_data, fake_client.id)

        mock_client_repo_instance.get_client_by_id.assert_called_once_with(mock_session, fake_client.id)
        mock_repository.get_name_pet_by_id_client.assert_called_once_with(mock_session, fake_client.id)
