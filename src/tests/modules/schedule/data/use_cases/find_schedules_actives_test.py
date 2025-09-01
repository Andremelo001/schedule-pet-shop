import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date, time

from src.modules.schedule.data.use_cases.find_schedules_actives import FindSchedulesActivesUseCase


@pytest.mark.asyncio
async def test_find_schedules_actives_success(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock active schedules exist
    mock_service_1 = MagicMock()
    mock_service_1.id = "service-id-1"
    
    mock_service_2 = MagicMock()
    mock_service_2.id = "service-id-2"

    mock_schedule_1 = MagicMock()
    mock_schedule_1.id = "schedule-id-1"
    mock_schedule_1.date_schedule = date(2024, 12, 25)
    mock_schedule_1.time_schedule = time(10, 30)
    mock_schedule_1.client_id = "client-id-1"
    mock_schedule_1.pet_id = "pet-id-1"
    mock_schedule_1.total_price_schedule = 100.0
    mock_schedule_1.schedule_active = True
    mock_schedule_1.services = [mock_service_1, mock_service_2]

    mock_schedule_2 = MagicMock()
    mock_schedule_2.id = "schedule-id-2"
    mock_schedule_2.date_schedule = date(2024, 12, 26)
    mock_schedule_2.time_schedule = time(14, 0)
    mock_schedule_2.client_id = "client-id-2"
    mock_schedule_2.pet_id = "pet-id-2"
    mock_schedule_2.total_price_schedule = 80.0
    mock_schedule_2.schedule_active = True
    mock_schedule_2.services = [mock_service_1]

    mock_repository.find_schedules_available.return_value = [mock_schedule_1, mock_schedule_2]

    use_case = FindSchedulesActivesUseCase(mock_repository)
    result = await use_case.find_schedules_actives(mock_session)

    assert len(result) == 2
    
    # Check first schedule
    assert result[0]["id"] == "schedule-id-1"
    assert result[0]["date_schedule"] == "2024-12-25"
    assert result[0]["time_schedule"] == "10:30:00"
    assert result[0]["client_id"] == "client-id-1"
    assert result[0]["pet_id"] == "pet-id-1"
    assert result[0]["total_price_schedule"] == 100.0
    assert result[0]["schedule_active"] == True
    assert result[0]["services"] == ["service-id-1", "service-id-2"]

    # Check second schedule
    assert result[1]["id"] == "schedule-id-2"
    assert result[1]["date_schedule"] == "2024-12-26"
    assert result[1]["time_schedule"] == "14:00:00"
    assert result[1]["client_id"] == "client-id-2"
    assert result[1]["pet_id"] == "pet-id-2"
    assert result[1]["total_price_schedule"] == 80.0
    assert result[1]["schedule_active"] == True
    assert result[1]["services"] == ["service-id-1"]

    mock_repository.find_schedules_available.assert_called_once_with(mock_session)


@pytest.mark.asyncio
async def test_find_schedules_actives_empty(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock no active schedules
    mock_repository.find_schedules_available.return_value = []

    use_case = FindSchedulesActivesUseCase(mock_repository)
    result = await use_case.find_schedules_actives(mock_session)

    assert len(result) == 0
    assert result == []

    mock_repository.find_schedules_available.assert_called_once_with(mock_session)


@pytest.mark.asyncio
async def test_find_schedules_actives_single_schedule(mocker):
    mock_repository = AsyncMock()
    mock_session = AsyncMock()

    # Mock single active schedule
    mock_service = MagicMock()
    mock_service.id = "service-id-1"

    mock_schedule = MagicMock()
    mock_schedule.id = "schedule-id-1"
    mock_schedule.date_schedule = date(2024, 12, 25)
    mock_schedule.time_schedule = time(9, 0)
    mock_schedule.client_id = "client-id-1"
    mock_schedule.pet_id = "pet-id-1"
    mock_schedule.total_price_schedule = 50.0
    mock_schedule.schedule_active = True
    mock_schedule.services = [mock_service]

    mock_repository.find_schedules_available.return_value = [mock_schedule]

    use_case = FindSchedulesActivesUseCase(mock_repository)
    result = await use_case.find_schedules_actives(mock_session)

    assert len(result) == 1
    assert result[0]["id"] == "schedule-id-1"
    assert result[0]["date_schedule"] == "2024-12-25"
    assert result[0]["time_schedule"] == "09:00:00"
    assert result[0]["client_id"] == "client-id-1"
    assert result[0]["pet_id"] == "pet-id-1"
    assert result[0]["total_price_schedule"] == 50.0
    assert result[0]["schedule_active"] == True
    assert result[0]["services"] == ["service-id-1"]

    mock_repository.find_schedules_available.assert_called_once_with(mock_session)
