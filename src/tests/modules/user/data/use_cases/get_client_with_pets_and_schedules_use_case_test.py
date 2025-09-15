import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date, time
from src.modules.user.data.use_cases.get_client_with_pets_and_schedules_use_case import GetClientWithPetsAndSchedulesUseCase
from src.errors.types_errors import HttpNotFoundError
from src.infra.db.entities.client import Client

@pytest.mark.asyncio
async def test_get_client_with_pets_and_schedules_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock pets
    mock_pet_1 = MagicMock()
    mock_pet_1.id = "pet-id-1"
    mock_pet_1.name = "Rex"
    mock_pet_1.breed = "Golden Retriever"
    mock_pet_1.age = 3
    mock_pet_1.size_in_centimeters = 60

    mock_pet_2 = MagicMock()
    mock_pet_2.id = "pet-id-2"
    mock_pet_2.name = "Luna"
    mock_pet_2.breed = "Labrador"
    mock_pet_2.age = 2
    mock_pet_2.size_in_centimeters = 55

    # Mock schedules
    mock_schedule_1 = MagicMock()
    mock_schedule_1.id = "schedule-id-1"
    mock_schedule_1.date_schedule = date(2024, 12, 25)
    mock_schedule_1.time_schedule = time(10, 30)
    mock_schedule_1.total_price_schedule = 100
    mock_schedule_1.schedule_active = True

    mock_schedule_2 = MagicMock()
    mock_schedule_2.id = "schedule-id-2"
    mock_schedule_2.date_schedule = date(2024, 12, 26)
    mock_schedule_2.time_schedule = time(14, 0)
    mock_schedule_2.total_price_schedule = 80
    mock_schedule_2.schedule_active = False

    # Mock client with pets and schedules
    mock_client_with_data = MagicMock()
    mock_client_with_data.id = "client-id-123"
    mock_client_with_data.name = "Andre"
    mock_client_with_data.cpf = "08855040383"
    mock_client_with_data.age = 25
    mock_client_with_data.email = "andre@gmail.com"
    mock_client_with_data.senha = "senha123"
    mock_client_with_data.pets = [mock_pet_1, mock_pet_2]
    mock_client_with_data.schedules = [mock_schedule_1, mock_schedule_2]

    mock_repository.get_client_with_pets_and_schedules_by_id.return_value = mock_client_with_data

    use_case = GetClientWithPetsAndSchedulesUseCase(mock_repository)

    result = await use_case.get_client_with_pets_and_schedules(mock_session, "client-id-123")

    # Verify client data
    assert result["id"] == "client-id-123"
    assert result["name"] == "Andre"
    assert result["cpf"] == "08855040383"
    assert result["age"] == 25
    assert result["email"] == "andre@gmail.com"

    # Verify pets data
    assert len(result["pets"]) == 2
    assert result["pets"][0]["id"] == "pet-id-1"
    assert result["pets"][0]["name"] == "Rex"
    assert result["pets"][0]["breed"] == "Golden Retriever"
    assert result["pets"][0]["age"] == 3
    assert result["pets"][0]["size_in_centimeters"] == 60

    assert result["pets"][1]["id"] == "pet-id-2"
    assert result["pets"][1]["name"] == "Luna"
    assert result["pets"][1]["breed"] == "Labrador"

    # Verify schedules data
    assert len(result["schedules"]) == 2
    assert result["schedules"][0]["id"] == "schedule-id-1"
    assert result["schedules"][0]["date_schedule"] == "2024-12-25"
    assert result["schedules"][0]["time_schedule"] == "10:30:00"
    assert result["schedules"][0]["total_price_schedule"] == 100
    assert result["schedules"][0]["schedule_active"] == True

    assert result["schedules"][1]["schedule_active"] == False

    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.get_client_with_pets_and_schedules_by_id.assert_called_once_with(mock_session, "client-id-123")

@pytest.mark.asyncio
async def test_get_client_with_pets_and_schedules_not_found(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client does not exist
    mock_repository.get_client_by_id.return_value = None

    use_case = GetClientWithPetsAndSchedulesUseCase(mock_repository)

    with pytest.raises(HttpNotFoundError) as exc_info:
        await use_case.get_client_with_pets_and_schedules(mock_session, "client-id-123")

    assert "Cliente com o id client-id-123 não encontrado" in str(exc_info.value)
    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")

@pytest.mark.asyncio
async def test_get_client_with_empty_pets_and_schedules(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock client exists
    fake_client = Client(id="client-id-123")
    mock_repository.get_client_by_id.return_value = fake_client

    # Mock client with no pets and schedules
    mock_client_with_data = MagicMock()
    mock_client_with_data.id = "client-id-123"
    mock_client_with_data.name = "Andre"
    mock_client_with_data.cpf = "08855040383"
    mock_client_with_data.age = 25
    mock_client_with_data.email = "andre@gmail.com"
    mock_client_with_data.senha = "senha123"
    mock_client_with_data.pets = []
    mock_client_with_data.schedules = []

    mock_repository.get_client_with_pets_and_schedules_by_id.return_value = mock_client_with_data

    use_case = GetClientWithPetsAndSchedulesUseCase(mock_repository)

    result = await use_case.get_client_with_pets_and_schedules(mock_session, "client-id-123")

    assert result["id"] == "client-id-123"
    assert result["name"] == "Andre"
    assert len(result["pets"]) == 0
    assert len(result["schedules"]) == 0

    mock_repository.get_client_by_id.assert_called_once_with(mock_session, "client-id-123")
    mock_repository.get_client_with_pets_and_schedules_by_id.assert_called_once_with(mock_session, "client-id-123")
