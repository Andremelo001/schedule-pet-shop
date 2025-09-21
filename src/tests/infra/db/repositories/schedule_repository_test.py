import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date, time
from src.infra.db.repositories.schedule_repository import ScheduleRepository
from src.modules.schedule.dto.schedule_dto import ScheduleDTO

@pytest.mark.asyncio
async def test_create_schedule(mocker):
    fake_schedule = ScheduleDTO(
        date_schedule=date(2024, 12, 25),
        time_schedule=time(10, 30),
        id_client="client-id-123",
        id_pet="pet-id-123",
        list_services=["service-id-1", "service-id-2"]
    )

    # Mock dos serviços para calcular preço total
    mock_service_1 = MagicMock()
    mock_service_1.price = 50.0
    
    mock_service_2 = MagicMock()
    mock_service_2.price = 30.0

    mock_service_result_1 = MagicMock()
    mock_service_result_1.scalar_one_or_none.return_value = mock_service_1
    
    mock_service_result_2 = MagicMock()
    mock_service_result_2.scalar_one_or_none.return_value = mock_service_2

    # Mock da entidade Schedule
    mock_schedule_entity = MagicMock()
    mock_schedule_entity.id = "new-schedule-id"
    
    # Mock da entidade ScheduleServices
    mock_schedule_services = MagicMock()

    with mocker.patch('src.infra.db.repositories.schedule_repository.ScheduleEntitie', return_value=mock_schedule_entity):
        with mocker.patch('src.infra.db.repositories.schedule_repository.ScheduleServices', return_value=mock_schedule_services):
            mock_session = AsyncMock()
            # Configura os retornos para as consultas de serviços
            mock_session.execute.side_effect = [mock_service_result_1, mock_service_result_2]

            repository = ScheduleRepository(mock_session)
            await repository.create_schedule(fake_schedule)

            # Verifica se as operações de persistência foram chamadas
            assert mock_session.add.call_count >= 3  # schedule + 2 associations
            assert mock_session.commit.call_count == 2
            assert mock_session.refresh.called

@pytest.mark.asyncio
async def test_find_email_client_by_id_schedule(mocker):
    fake_schedule_id = "schedule-id-123"
    fake_email = "client@email.com"

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_email

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    email = await repository.find_email_client_by_id_schedule(fake_schedule_id)

    assert email == fake_email
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find_schedule_by_id(mocker):
    fake_id = "schedule-id-123"
    fake_schedule = MagicMock()
    fake_schedule.id = fake_id

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_schedule

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    schedule = await repository.find_schedule_by_id(fake_id)

    assert schedule.id == fake_id
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_list_schedules(mocker):
    fake_schedule_1 = MagicMock()
    fake_schedule_1.id = "schedule-1"
    
    fake_schedule_2 = MagicMock()
    fake_schedule_2.id = "schedule-2"
    
    fake_schedules = [fake_schedule_1, fake_schedule_2]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_schedules

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    schedules = await repository.list_schedules()

    assert len(schedules) == 2
    assert schedules[0].id == "schedule-1"
    assert schedules[1].id == "schedule-2"
    mock_session.execute.assert_called_once()

    assert len(schedules) == 2
    assert schedules[0].id == "schedule-1"
    assert schedules[1].id == "schedule-2"
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find_schedule_by_id_client(mocker):
    fake_client_id = "client-id-123"
    fake_schedule_1 = MagicMock()
    fake_schedule_1.client_id = fake_client_id
    
    fake_schedule_2 = MagicMock()
    fake_schedule_2.client_id = fake_client_id
    
    fake_schedules = [fake_schedule_1, fake_schedule_2]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_schedules

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    schedules = await repository.find_schedule_by_id_client(fake_client_id)

    assert len(schedules) == 2
    assert all(schedule.client_id == fake_client_id for schedule in schedules)
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_schedule(mocker):
    fake_schedule_id = "schedule-id-123"
    fake_schedule = MagicMock()
    fake_schedule.id = fake_schedule_id
    fake_schedule.schedule_active = True

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_schedule

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    await repository.cancel_schedule(fake_schedule_id)

    assert fake_schedule.schedule_active == False
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called

@pytest.mark.asyncio
async def test_find_schedules_available(mocker):
    fake_schedule_1 = MagicMock()
    fake_schedule_1.id = "schedule-1"
    fake_schedule_1.schedule_active = True
    
    fake_schedule_2 = MagicMock()
    fake_schedule_2.id = "schedule-2"
    fake_schedule_2.schedule_active = True
    
    fake_schedules = [fake_schedule_1, fake_schedule_2]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_schedules

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    schedules = await repository.find_schedules_available()

    assert len(schedules) == 2
    assert all(schedule.schedule_active == True for schedule in schedules)
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_delete_schedule(mocker):
    fake_schedule_id = "schedule-id-123"
    fake_schedule = MagicMock()
    fake_schedule.id = fake_schedule_id

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_schedule

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    await repository.delete_schedule(fake_schedule_id)

    assert mock_session.execute.called
    assert mock_session.delete.called
    assert mock_session.commit.called

@pytest.mark.asyncio
async def test_duration_services_in_schedule(mocker):
    fake_service_ids = ["service-id-1", "service-id-2"]
    
    # Mock dos serviços com durações específicas
    mock_service_1 = MagicMock()
    mock_service_1.duration_in_minutes = 60
    
    mock_service_2 = MagicMock()
    mock_service_2.duration_in_minutes = 30

    mock_service_result_1 = MagicMock()
    mock_service_result_1.scalar_one_or_none.return_value = mock_service_1
    
    mock_service_result_2 = MagicMock()
    mock_service_result_2.scalar_one_or_none.return_value = mock_service_2

    mock_session = AsyncMock()
    mock_session.execute.side_effect = [mock_service_result_1, mock_service_result_2]

    repository = ScheduleRepository(mock_session)
    total_duration = await repository.duration_services_in_schedule(fake_service_ids)

    assert total_duration == 90  # 60 + 30
    assert mock_session.execute.call_count == 2

@pytest.mark.asyncio
async def test_get_service_ids_from_schedule(mocker):
    fake_schedule_id = "schedule-id-123"
    fake_service_ids = ["service-id-1", "service-id-2"]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_service_ids

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    service_ids = await repository.get_service_ids_from_schedule(fake_schedule_id)

    assert len(service_ids) == 2
    assert service_ids == ["service-id-1", "service-id-2"]
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find_schedules_by_date(mocker):
    fake_date = date(2024, 12, 25)
    fake_schedule_1 = MagicMock()
    fake_schedule_1.date_schedule = fake_date
    fake_schedule_1.schedule_active = True
    
    fake_schedule_2 = MagicMock()
    fake_schedule_2.date_schedule = fake_date
    fake_schedule_2.schedule_active = True
    
    fake_schedules = [fake_schedule_1, fake_schedule_2]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_schedules

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    repository = ScheduleRepository(mock_session)
    schedules = await repository.find_schedules_by_date(fake_date)

    assert len(schedules) == 2
    assert all(schedule.date_schedule == fake_date for schedule in schedules)
    assert all(schedule.schedule_active == True for schedule in schedules)
    mock_session.execute.assert_called_once()