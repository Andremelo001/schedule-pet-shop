from typing import Dict, List
from datetime import datetime, time, timedelta, date
from src.modules.schedule.dto.schedule_dto import ScheduleDTO
from src.errors.error_handler import HttpUnauthorized
from src.modules.schedule.domain.use_cases.interface_schedule_create import InterfaceScheduleCreateUsecase
from src.modules.schedule.data.interfaces.interface_schedule_repository import InterfaceScheduleRepository

class ScheduleCreateUseCase(InterfaceScheduleCreateUsecase):
    def __init__(self, repository: InterfaceScheduleRepository):
        self.__repository = repository

    async def create(self, schedule: ScheduleDTO) -> Dict:

        await self.__validate_temp_services_in_schedule(schedule)

        await self.__validate_pet_exists(schedule.id_pet, schedule.id_client)

        self.__validate_time_schedule(schedule.time_schedule)

        self.__validate_data_schedule(schedule.date_schedule)

        self.__validate_total_services_in_schedule(schedule.list_services)

        await self.__validate_schedule_conflicts(schedule)

        return await self.__register_schedule_informations(schedule)
    
    async def __validate_pet_exists(self, pet_id: str, id_client: str) -> None:

        ids_pets = await self.__repository.list_id_pets_by_client(id_client)

        if pet_id not in ids_pets:
            raise HttpUnauthorized(f"O pet informado não é um pet do cliente {id_client}") 

    async def __validate_temp_services_in_schedule(self, schedule: ScheduleDTO) -> None:

        temp_total_in_minutes = await self.__repository.duration_services_in_schedule(schedule.list_services)

        if temp_total_in_minutes > 120:
            raise HttpUnauthorized("Quantidade total de tempo dos serviços extrapola a quantidade total permitida.")
        
    @classmethod
    def __validate_time_schedule(cls, time_schedule: time) -> None:

        if time_schedule.minute !=  0:
            raise HttpUnauthorized("Horários quebrados não são aceitos. Informe um horário cheio (ex.: 08:00, 13:00)")

        intervalos_validos = [
            (time(hour=8, minute=0), time(hour=12, minute=0)),
            (time(hour=14, minute=0), time(hour=18, minute=0))
        ]

        if not any(inicio <= time_schedule <= fim for inicio, fim in intervalos_validos):
            raise HttpUnauthorized("Horário cadastrado não é válido, trabalhamos das 8:00 as 12:00 e das 14:00 as 18:00")    

    @classmethod
    def __validate_data_schedule(cls, date_schedule: date) -> None:

        dia_semana = date_schedule.weekday()

        if dia_semana >= 6:
            raise HttpUnauthorized("Não trabalhamos aos domingos, altere a data do agendamento para um dia válido")

    @classmethod
    def __validate_total_services_in_schedule(cls, list_services: List[str]) -> None:

        total_services = len(list_services)

        if total_services > 3:
            raise HttpUnauthorized("Só são permitidos 3 serviços por agendamento!")

    async def __validate_schedule_conflicts(self, schedule: ScheduleDTO) -> None:

        existing_schedules = await self.__repository.find_schedules_by_date(schedule.date_schedule)
        
        new_schedule_duration = await self.__repository.duration_services_in_schedule(schedule.list_services)
        
        new_start_time = datetime.combine(schedule.date_schedule, schedule.time_schedule)

        new_end_time = new_start_time + timedelta(minutes=new_schedule_duration)
        
        for existing in existing_schedules:
            
            existing_start = datetime.combine(existing.date_schedule, existing.time_schedule)
            
            existing_service_ids = await self.__repository.get_service_ids_from_schedule(str(existing.id))
            
            existing_duration = await self.__repository.duration_services_in_schedule(existing_service_ids)

            existing_end = existing_start + timedelta(minutes=existing_duration)
            
            blocked_until = self.__calculate_next_available_slot(existing_end)
            
            if self.__has_time_conflict(new_start_time, new_end_time, existing_start, blocked_until):
                next_available = blocked_until.strftime("%H:%M")
                raise HttpUnauthorized(
                    f"Horário não disponível. O próximo horário disponível é às {next_available}."
                )

    @classmethod
    def __calculate_next_available_slot(cls, end_time: datetime) -> datetime:

        if end_time.minute == 0:
            return end_time
        
        next_hour = end_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        return next_hour

    @classmethod
    def __has_time_conflict(cls, new_start: datetime, new_end: datetime, 
                          existing_start: datetime, blocked_until: datetime) -> bool:

        if new_start < blocked_until:
            return True
        
        if new_start < existing_start and new_end > existing_start:
            return True
            
        return False
    
    async def __register_schedule_informations(self, pet: ScheduleDTO) -> Dict:

        await self.__repository.create_schedule(pet)

        return {"mensagem": "Agendamento cadastrado com Sucesso"}