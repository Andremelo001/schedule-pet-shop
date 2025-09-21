import pytest
from unittest.mock import AsyncMock, MagicMock
from src.infra.db.entities.pet import Pet
from src.infra.db.repositories.pet_repository import PetRepository
from src.modules.pet.dto.pet_dto import PetDTO, PetUpdateDTO

@pytest.mark.asyncio
async def test_create_pet(mocker):
    fake_client_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_pet = PetDTO(
        id_client="69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef",
        name="Rex",
        breed="Golden Retriever",
        age=3,
        size_in_centimeters=60
    )

    mock_session = AsyncMock()

    repository = PetRepository(mock_session)
    await repository.create_pet(fake_client_id, fake_pet)

    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called

    # Acessa o pet adicionado
    added_pet = mock_session.add.call_args[0][0]
    assert added_pet.name == fake_pet.name
    assert added_pet.breed == fake_pet.breed
    assert added_pet.age == fake_pet.age
    assert added_pet.size_in_centimeters == fake_pet.size_in_centimeters
    assert added_pet.client_id == fake_client_id

@pytest.mark.asyncio
async def test_delete_pet(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_pet = Pet(id=fake_id)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_pet

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = PetRepository(mock_session)
    await repository.delete_pet(fake_id)

    assert mock_session.execute.called
    assert mock_session.delete.called
    assert mock_session.commit.called

@pytest.mark.asyncio
async def test_uptdate_pet(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_pet = Pet(id=fake_id, name="Rex", breed="Golden", age=3, size_in_centimeters=60)

    update_data = PetUpdateDTO(
        name="Max",
        breed="Labrador",
        age=4,
        size_in_centimeters="65"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_pet

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = PetRepository(mock_session)
    updated_pet = await repository.uptdate_pet(fake_id, update_data)

    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert updated_pet.name == "Max"
    assert updated_pet.breed == "Labrador"
    assert updated_pet.age == 4
    assert updated_pet.size_in_centimeters == "65"

@pytest.mark.asyncio
async def test_get_pet(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_pet = Pet(id=fake_id)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_pet

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = PetRepository(mock_session)
    pet = await repository.get_pet(fake_id)

    assert pet.id == fake_id
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_pets_by_cpf_client(mocker):
    fake_cpf = "12345678909"
    fake_pets = [Pet(name="Rex"), Pet(name="Max")]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_pets

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = PetRepository(mock_session)
    pets = await repository.get_all_pets_by_cpf_client(fake_cpf)

    assert len(pets) == 2
    assert pets[0].name == "Rex"
    assert pets[1].name == "Max"
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_name_pet_by_id_client(mocker):
    fake_client_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_names = ["Rex", "Max", "Luna"]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_names

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = PetRepository(mock_session)
    names = await repository.get_name_pet_by_id_client(fake_client_id)

    assert len(names) == 3
    assert names == ["Rex", "Max", "Luna"]
    mock_session.execute.assert_called_once()