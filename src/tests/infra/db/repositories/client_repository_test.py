import pytest
from unittest.mock import AsyncMock, MagicMock
from src.infra.db.entities.client import Client
from src.infra.db.repositories.client_repository import ClientRepository
from src.dto.client_dto import ClientDTO, ClientUpdateDTO

@pytest.mark.asyncio
async def test_get_client(mocker):
    fake_cpf = "08855040383"
    fake_client = Client(cpf=fake_cpf)

    #simula o retorno da query session.execute
    #finge que a query de busca foi executada e retornou um cliente
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    #simula uma instancia da AssyncSession
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    client = await ClientRepository.get_client(mock_session, fake_cpf)

    assert client.cpf == fake_cpf
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_create_client(mocker):
    fake_client = ClientDTO(
        name= "Andre",
        cpf= "088550540383",
        age= 20,
        email= "de@gmail.com",
        senha= "de2019"
    )

    mock_session = AsyncMock()

    await ClientRepository.create_client(mock_session, fake_client)

    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called

    #acessa o cliente
    added_client = mock_session.add.call_args[0][0]
    assert added_client.cpf == fake_client.cpf
    assert added_client.name == fake_client.name
    assert added_client.is_admin is False


@pytest.mark.asyncio
async def test_get_client_by_id(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_client = Client(id=fake_id)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_client

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    client = await ClientRepository.get_client_by_id(mock_session, fake_id)

    assert client.id == fake_id
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_delete_client(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_client = Client(id=fake_id)

    mock_session = AsyncMock()

    repository = ClientRepository()

    #mocka o método de busca get_client_by_id para retornar um cliente
    repository.get_client_by_id = AsyncMock(return_value=fake_client)

    await repository.delete_client(mock_session, fake_id)

    assert mock_session.delete.called
    assert mock_session.commit.called

@pytest.mark.asyncio
async def test_update_client(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_client = Client(id=fake_id)

    update_data = ClientUpdateDTO(
        name= "Andre",
        cpf= "088550540383",
        age= 20,
        email= "de@gmail.com",
        senha= "de2019"
    )

    repository = ClientRepository()

    mock_session = AsyncMock()

    repository.get_client_by_id = AsyncMock(return_value=fake_client)

    update_client = await repository.update_client(mock_session, fake_id, update_data)

    assert mock_session.commit.called
    assert mock_session.refresh.called

    assert update_client.name == "Andre"
    assert update_client.cpf == "088550540383"
    assert update_client.age == 20
    assert update_client.email == "de@gmail.com"
    assert update_client.senha == "de2019"




