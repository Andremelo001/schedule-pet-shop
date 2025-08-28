import pytest
from unittest.mock import AsyncMock, MagicMock
from src.infra.db.repositories.service_repository import ServiceRepository
from src.modules.service_types.dto.service_dto import ServiceDTO, UpdateServiceDTO

@pytest.mark.asyncio
async def test_create_service(mocker):
    fake_service = ServiceDTO(
        duration_in_minutes=60,
        type_service="Banho e Tosa",
        price=50.0
    )

    mock_service_entity = MagicMock()
    mock_service_entity.duration_in_minutes = fake_service.duration_in_minutes
    mock_service_entity.type_service = fake_service.type_service
    mock_service_entity.price = fake_service.price

    # Patch da classe ServicesEntitie
    with mocker.patch('src.infra.db.repositories.service_repository.ServicesEntitie', return_value=mock_service_entity):
        mock_session = AsyncMock()

        await ServiceRepository.create_service(mock_session, fake_service)

        assert mock_session.add.called
        assert mock_session.commit.called
        assert mock_session.refresh.called

        # Acessa o serviço adicionado
        added_service = mock_session.add.call_args[0][0]
        assert added_service.duration_in_minutes == fake_service.duration_in_minutes
        assert added_service.type_service == fake_service.type_service
        assert added_service.price == fake_service.price

@pytest.mark.asyncio
async def test_find_service_by_id(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_service = MagicMock()
    fake_service.id = fake_id
    fake_service.type_service = "Banho e Tosa"

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_service

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    service = await ServiceRepository.find_service_by_id(mock_session, fake_id)

    assert service.id == fake_id
    assert service.type_service == "Banho e Tosa"
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_list_services(mocker):
    fake_service_1 = MagicMock()
    fake_service_1.type_service = "Banho e Tosa"
    fake_service_1.price = 50.0
    
    fake_service_2 = MagicMock()
    fake_service_2.type_service = "Consulta Veterinária"
    fake_service_2.price = 80.0
    
    fake_services = [fake_service_1, fake_service_2]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_services

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    services = await ServiceRepository.list_services(mock_session)

    assert len(services) == 2
    assert services[0].type_service == "Banho e Tosa"
    assert services[1].type_service == "Consulta Veterinária"
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_update_service(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_service = MagicMock()
    fake_service.id = fake_id
    fake_service.duration_in_minutes = 60
    fake_service.type_service = "Banho"
    fake_service.price = 40.0

    update_data = UpdateServiceDTO(
        duration_in_minutes=90,
        type_service="Banho e Tosa",
        price=60.0
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_service

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ServiceRepository()
    updated_service = await repository.update_service(mock_session, update_data, fake_id)

    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert updated_service.duration_in_minutes == 90
    assert updated_service.type_service == "Banho e Tosa"
    assert updated_service.price == 60.0

@pytest.mark.asyncio
async def test_delete_service(mocker):
    fake_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    fake_service = MagicMock()
    fake_service.id = fake_id

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_service

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ServiceRepository()
    await repository.delete_service(mock_session, fake_id)

    assert mock_session.execute.called
    assert mock_session.delete.called
    assert mock_session.commit.called

@pytest.mark.asyncio
async def test_get_schedules_by_service_id(mocker):
    fake_service_id = "69bde4f5-c54f-47d0-9c65-ea9d3dbd0eef"
    
    fake_schedule_1 = MagicMock()
    fake_schedule_1.id = "schedule1"
    
    fake_schedule_2 = MagicMock()
    fake_schedule_2.id = "schedule2"
    
    fake_schedules = [fake_schedule_1, fake_schedule_2]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_schedules

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ServiceRepository()
    schedules = await repository.get_schedules_by_service_id(mock_session, fake_service_id)

    assert len(schedules) == 2
    assert schedules[0].id == "schedule1"
    assert schedules[1].id == "schedule2"
    mock_session.execute.assert_called_once()