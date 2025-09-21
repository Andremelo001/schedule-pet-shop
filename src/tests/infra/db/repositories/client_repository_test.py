import pytest
from unittest.mock import AsyncMock, MagicMock
from src.infra.db.entities.client import Client
from src.infra.db.repositories.client_repository import ClientRepository
from src.modules.user.dto.client_dto import ClientDTO, ClientUpdateDTO

@pytest.mark.asyncio
async def test_get_client(mocker):
    fake_cpf = "12345678909"
    fake_client = Client(cpf=fake_cpf)

    #simula o retorno da query session.execute
    #finge que a query de busca foi executada e retornou um cliente
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    #simula uma instancia da AssyncSession
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ClientRepository(mock_session)
    client = await repository.get_client(fake_cpf)

    assert client.cpf == fake_cpf
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_create_client(mocker):
    fake_client = ClientDTO(
        name= "Andre",
        cpf= "12345678909",
        age= 20,
        email= "de@gmail.com",
        senha= "de2019"
    )

    mock_session = AsyncMock()

    repository = ClientRepository(mock_session)
    await repository.create_client(fake_client)

    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called

    #acessa o cliente
    added_client = mock_session.add.call_args[0][0]
    assert added_client.cpf == fake_client.cpf
    assert added_client.name == fake_client.name


@pytest.mark.asyncio
async def test_get_client_by_id(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_client = Client(id=fake_id)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ClientRepository(mock_session)
    client = await repository.get_client_by_id(fake_id)

    assert client.id == fake_id
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_delete_client(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_client = Client(id=fake_id)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ClientRepository(mock_session)
    await repository.delete_client(fake_id)

    assert mock_session.execute.called
    assert mock_session.delete.called
    assert mock_session.commit.called

@pytest.mark.asyncio
async def test_update_client(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_client = MagicMock()
    fake_client.id = fake_id
    
    # Configure as propriedades iniciais
    fake_client.name = "Old Name"
    fake_client.cpf = "12345678909"
    fake_client.age = 18
    fake_client.email = "old@gmail.com"
    fake_client.senha = "old123"

    update_data = ClientUpdateDTO(
        name= "Andre",
        cpf= "12345678909", 
        age= 20,
        email= "de@gmail.com",
        senha= "de2019"
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ClientRepository(mock_session)
    update_client = await repository.update_client(fake_id, update_data)

    assert mock_session.commit.called
    assert mock_session.refresh.called

    # Apenas verifica se o cliente retornado é o mesmo objeto mockado
    assert update_client == fake_client

@pytest.mark.asyncio
async def test_get_client_by_email(mocker):
    fake_email = "de@gmail.com"
    fake_client = Client(email=fake_email)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ClientRepository(mock_session)
    client = await repository.get_client_by_email(fake_email)

    assert client.email == fake_email
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_client_with_pets_and_schedules_by_id(mocker):
    from src.infra.db.entities.client import ClientWithPetsWithSchedules
    
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_client = ClientWithPetsWithSchedules(id=fake_id, name="Andre", cpf="12345678909", age=20, email="de@gmail.com", senha="de2019")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ClientRepository(mock_session)
    client = await repository.get_client_with_pets_and_schedules_by_id(fake_id)

    assert str(client.id) == fake_id
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find_schedule_by_id_client(mocker):
    from src.infra.db.entities.schedule import Schedule as ScheduleEntity
    
    fake_client_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_schedules = [ScheduleEntity(client_id=fake_client_id), ScheduleEntity(client_id=fake_client_id)]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_schedules

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ClientRepository(mock_session)
    schedules = await repository.find_schedule_by_id_client(fake_client_id)

    assert len(schedules) == 2
    assert all(schedule.client_id == fake_client_id for schedule in schedules)
    mock_session.execute.assert_called_once()




