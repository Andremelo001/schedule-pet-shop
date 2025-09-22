import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, time, date

from src.modules.schedule.data.use_cases.schedule_create_use_case import ScheduleCreateUseCase
from src.modules.schedule.dto.schedule_dto import ScheduleDTO
from src.errors.error_handler import HttpUnauthorized


@pytest.mark.asyncio
async def test_create_schedule_success(mocker):
    mock_repository = AsyncMock()

    # Mock valid schedule data
    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123", 
        list_services=["service-1", "service-2"],
        date_schedule=date(2024, 12, 10),  # Tuesday
        time_schedule=time(8, 0)
    )

    # Mock repository methods
    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation
    mock_repository.duration_services_in_schedule.return_value = 90  # 90 minutes total
    mock_repository.find_schedules_by_date.return_value = []  # No conflicts
    mock_repository.create_schedule.return_value = None

    use_case = ScheduleCreateUseCase(mock_repository)
    result = await use_case.create( schedule_dto)

    assert result == {"mensagem": "Agendamento cadastrado com Sucesso"}
    mock_repository.create_schedule.assert_called_once_with( schedule_dto)


@pytest.mark.asyncio
async def test_create_schedule_temp_services_exceed_limit(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1", "service-2", "service-3"],
        date_schedule=date(2024, 12, 10),
        time_schedule=time(8, 0)
    )

    # Mock duration exceeding 120 minutes
    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation

    mock_repository.duration_services_in_schedule.return_value = 150

    use_case = ScheduleCreateUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Quantidade total de tempo dos serviços extrapola a quantidade total permitida."):
        await use_case.create( schedule_dto)


@pytest.mark.asyncio
async def test_create_schedule_invalid_time_broken_hour(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1"],
        date_schedule=date(2024, 12, 10),
        time_schedule=time(8, 30)  # Broken hour - not allowed
    )

    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation


    mock_repository.duration_services_in_schedule.return_value = 60

    use_case = ScheduleCreateUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Horários quebrados não são aceitos. Informe um horário cheio"):
        await use_case.create( schedule_dto)


@pytest.mark.asyncio
async def test_create_schedule_invalid_time_outside_working_hours(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1"],
        date_schedule=date(2024, 12, 10),
        time_schedule=time(19, 0)  # Outside working hours
    )

    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation


    mock_repository.duration_services_in_schedule.return_value = 60

    use_case = ScheduleCreateUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Horário cadastrado não é válido, trabalhamos das 8:00 as 12:00 e das 14:00 as 18:00"):
        await use_case.create( schedule_dto)


@pytest.mark.asyncio
async def test_create_schedule_sunday_not_allowed(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1"],
        date_schedule=date(2024, 12, 8),  # Sunday
        time_schedule=time(8, 0)
    )

    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation


    mock_repository.duration_services_in_schedule.return_value = 60

    use_case = ScheduleCreateUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Não trabalhamos aos domingos, altere a data do agendamento para um dia válido"):
        await use_case.create( schedule_dto)


@pytest.mark.asyncio
async def test_create_schedule_too_many_services(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1", "service-2", "service-3", "service-4"],  # 4 services - too many
        date_schedule=date(2024, 12, 10),
        time_schedule=time(8, 0)
    )

    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation


    mock_repository.duration_services_in_schedule.return_value = 60

    use_case = ScheduleCreateUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Só são permitidos 3 serviços por agendamento!"):
        await use_case.create( schedule_dto)


@pytest.mark.asyncio
async def test_create_schedule_time_conflict(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1"],
        date_schedule=date(2024, 12, 10),
        time_schedule=time(8, 0)
    )

    # Mock existing schedule that conflicts
    existing_schedule = MagicMock()
    existing_schedule.id = "existing-123"
    existing_schedule.date_schedule = date(2024, 12, 10)
    existing_schedule.time_schedule = time(8, 0)

    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation
    mock_repository.duration_services_in_schedule.return_value = 60
    mock_repository.find_schedules_by_date.return_value = [existing_schedule]
    mock_repository.get_service_ids_from_schedule.return_value = ["existing-service"]

    use_case = ScheduleCreateUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Horário não disponível. Intervalos disponíveis no dia:"):
        await use_case.create( schedule_dto)


@pytest.mark.asyncio
async def test_create_schedule_valid_working_hours_morning(mocker):
    mock_repository = AsyncMock()

    # Test valid morning hours
    for hour in [8, 9, 10, 11, 12]:
        schedule_dto = ScheduleDTO(
            id_client="client-123",
            id_pet="pet-123",
            list_services=["service-1"],
            date_schedule=date(2024, 12, 10),
            time_schedule=time(hour, 0)
        )

        mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation


        mock_repository.duration_services_in_schedule.return_value = 60
        mock_repository.find_schedules_by_date.return_value = []
        mock_repository.create_schedule.return_value = None

        use_case = ScheduleCreateUseCase(mock_repository)
        result = await use_case.create( schedule_dto)

        assert result == {"mensagem": "Agendamento cadastrado com Sucesso"}


@pytest.mark.asyncio
async def test_create_schedule_valid_working_hours_afternoon(mocker):
    mock_repository = AsyncMock()

    # Test valid afternoon hours
    for hour in [14, 15, 16, 17, 18]:
        schedule_dto = ScheduleDTO(
            id_client="client-123",
            id_pet="pet-123",
            list_services=["service-1"],
            date_schedule=date(2024, 12, 10),
            time_schedule=time(hour, 0)
        )

        mock_repository.list_id_pets_by_client.return_value = ["pet-123"]  # Mock pet validation


        mock_repository.duration_services_in_schedule.return_value = 60
        mock_repository.find_schedules_by_date.return_value = []
        mock_repository.create_schedule.return_value = None

        use_case = ScheduleCreateUseCase(mock_repository)
        result = await use_case.create( schedule_dto)

        assert result == {"mensagem": "Agendamento cadastrado com Sucesso"}


@pytest.mark.asyncio
async def test_create_schedule_time_conflict_with_available_intervals(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1"],
        date_schedule=date(2024, 12, 10),
        time_schedule=time(9, 0)  # Trying to schedule at 9:00
    )

    # Mock existing schedule that conflicts (8:00-10:00)
    existing_schedule = MagicMock()
    existing_schedule.id = "existing-123"
    existing_schedule.date_schedule = date(2024, 12, 10)
    existing_schedule.time_schedule = time(8, 0)

    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]
    mock_repository.find_schedules_by_date.return_value = [existing_schedule]
    mock_repository.get_service_ids_from_schedule.return_value = ["existing-service"]
    
    # Configure different durations for new schedule vs existing schedule
    def mock_duration(service_list):
        if service_list == ["service-1"]:  # New schedule
            return 60  # 1 hour
        elif service_list == ["existing-service"]:  # Existing schedule
            return 120  # 2 hours (8:00-10:00)
        return 60
    
    mock_repository.duration_services_in_schedule.side_effect = mock_duration

    use_case = ScheduleCreateUseCase(mock_repository)

    with pytest.raises(HttpUnauthorized, match="Horário não disponível. Intervalos disponíveis no dia:"):
        await use_case.create(schedule_dto)

    # Verify all necessary methods were called
    mock_repository.list_id_pets_by_client.assert_called_once_with("client-123")
    mock_repository.find_schedules_by_date.assert_called_once_with(date(2024, 12, 10))
    # O método get_service_ids_from_schedule pode ser chamado múltiplas vezes na nova lógica
    assert mock_repository.get_service_ids_from_schedule.call_count >= 1


@pytest.mark.asyncio 
async def test_create_schedule_no_conflicts_empty_day(mocker):
    mock_repository = AsyncMock()

    schedule_dto = ScheduleDTO(
        id_client="client-123",
        id_pet="pet-123",
        list_services=["service-1"],
        date_schedule=date(2024, 12, 10),
        time_schedule=time(10, 0)
    )

    mock_repository.list_id_pets_by_client.return_value = ["pet-123"]
    mock_repository.duration_services_in_schedule.return_value = 60
    mock_repository.find_schedules_by_date.return_value = []  # No existing schedules
    mock_repository.create_schedule.return_value = None

    use_case = ScheduleCreateUseCase(mock_repository)
    result = await use_case.create(schedule_dto)

    assert result == {"mensagem": "Agendamento cadastrado com Sucesso"}
    mock_repository.create_schedule.assert_called_once_with(schedule_dto)


def test_validate_time_schedule_valid_times():
    # Test valid times
    valid_times = [
        time(8, 0), time(9, 0), time(10, 0), time(11, 0), time(12, 0),
        time(14, 0), time(15, 0), time(16, 0), time(17, 0), time(18, 0)
    ]
    
    for valid_time in valid_times:
        # Should not raise exception
        ScheduleCreateUseCase._ScheduleCreateUseCase__validate_time_schedule(valid_time)


def test_validate_data_schedule_valid_weekdays():
    # Test valid weekdays (Monday = 0, Saturday = 5)
    valid_dates = [
        date(2024, 12, 9),   # Monday
        date(2024, 12, 10),  # Tuesday
        date(2024, 12, 11),  # Wednesday
        date(2024, 12, 12),  # Thursday
        date(2024, 12, 13),  # Friday
        date(2024, 12, 14),  # Saturday
    ]
    
    for valid_date in valid_dates:
        # Should not raise exception
        ScheduleCreateUseCase._ScheduleCreateUseCase__validate_data_schedule(valid_date)


def test_validate_total_services_valid_counts():
    # Test valid service counts (1, 2, 3)
    valid_service_lists = [
        ["service-1"],
        ["service-1", "service-2"],
        ["service-1", "service-2", "service-3"]
    ]
    
    for service_list in valid_service_lists:
        # Should not raise exception
        ScheduleCreateUseCase._ScheduleCreateUseCase__validate_total_services_in_schedule(service_list)


def test_format_available_intervals():
    # Test formatting of available intervals
    intervals = [
        (datetime(2024, 12, 10, 8, 0), datetime(2024, 12, 10, 10, 0)),
        (datetime(2024, 12, 10, 14, 0), datetime(2024, 12, 10, 16, 0))
    ]
    
    result = ScheduleCreateUseCase._ScheduleCreateUseCase__format_available_intervals(intervals)
    expected = "08:00 às 10:00, 14:00 às 16:00"
    assert result == expected


def test_format_available_intervals_empty():
    # Test formatting with no available intervals
    intervals = []
    
    result = ScheduleCreateUseCase._ScheduleCreateUseCase__format_available_intervals(intervals)
    expected = "Nenhum horário disponível no dia"
    assert result == expected


def test_adjust_intervals_to_full_hours():
    # Test adjustment of intervals to full hours
    intervals = [
        (datetime(2024, 12, 10, 8, 30), datetime(2024, 12, 10, 10, 45)),
        (datetime(2024, 12, 10, 14, 0), datetime(2024, 12, 10, 16, 0))
    ]
    
    result = ScheduleCreateUseCase._ScheduleCreateUseCase__adjust_intervals_to_full_hours(intervals)
    expected = [
        (datetime(2024, 12, 10, 9, 0), datetime(2024, 12, 10, 10, 0)),
        (datetime(2024, 12, 10, 14, 0), datetime(2024, 12, 10, 16, 0))
    ]
    assert result == expected
