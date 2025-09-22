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
        
        # Verificar se há conflito com agendamentos existentes
        has_conflict = await self.__check_schedule_conflict(new_start_time, new_end_time, existing_schedules)
        
        if has_conflict:
            available_intervals = await self.__get_available_time_intervals(schedule.date_schedule, existing_schedules)
            intervals_text = self.__format_available_intervals(available_intervals)
            raise HttpUnauthorized(
                f"Horário não disponível. Intervalos disponíveis no dia: {intervals_text}"
            )

    async def __check_schedule_conflict(self, new_start: datetime, new_end: datetime, existing_schedules: List) -> bool:
        """Verifica se há conflito com agendamentos existentes"""
        
        for existing in existing_schedules:
            existing_start = datetime.combine(existing.date_schedule, existing.time_schedule)
            
            existing_service_ids = await self.__repository.get_service_ids_from_schedule(str(existing.id))
            existing_duration = await self.__repository.duration_services_in_schedule(existing_service_ids)
            existing_end = existing_start + timedelta(minutes=existing_duration)
            
            # Verifica se há sobreposição de horários
            if (new_start < existing_end and new_end > existing_start):
                return True
                
        return False

    async def __get_available_time_intervals(self, schedule_date: date, existing_schedules: List) -> List[tuple]:
        """Calcula os intervalos de tempo disponíveis no dia"""
        
        # Horários de funcionamento
        morning_start = datetime.combine(schedule_date, time(8, 0))
        morning_end = datetime.combine(schedule_date, time(12, 0))
        afternoon_start = datetime.combine(schedule_date, time(14, 0))
        afternoon_end = datetime.combine(schedule_date, time(18, 0))
        
        # Coletar todos os intervalos ocupados
        occupied_intervals = []
        
        for existing in existing_schedules:
            existing_start = datetime.combine(existing.date_schedule, existing.time_schedule)
            
            existing_service_ids = await self.__repository.get_service_ids_from_schedule(str(existing.id))
            existing_duration = await self.__repository.duration_services_in_schedule(existing_service_ids)
            existing_end = existing_start + timedelta(minutes=existing_duration)
            
            occupied_intervals.append((existing_start, existing_end))
        
        # Ordenar intervalos ocupados por horário de início
        occupied_intervals.sort(key=lambda x: x[0])
        
        # Calcular intervalos disponíveis
        available_intervals = []
        
        # Verificar período da manhã
        morning_intervals = self.__calculate_free_intervals_in_period(morning_start, morning_end, occupied_intervals)
        available_intervals.extend(morning_intervals)
        
        # Verificar período da tarde
        afternoon_intervals = self.__calculate_free_intervals_in_period(afternoon_start, afternoon_end, occupied_intervals)
        available_intervals.extend(afternoon_intervals)
        
        # Ajustar intervalos para horários cheios (sem minutos quebrados)
        adjusted_intervals = self.__adjust_intervals_to_full_hours(available_intervals)
        
        return adjusted_intervals

    @classmethod
    def __calculate_free_intervals_in_period(cls, period_start: datetime, period_end: datetime, 
                                           occupied_intervals: List[tuple]) -> List[tuple]:
        """Calcula intervalos livres dentro de um período específico"""
        
        free_intervals = []
        current_time = period_start
        
        for occupied_start, occupied_end in occupied_intervals:
            # Se o agendamento está fora do período, pular
            if occupied_end <= period_start or occupied_start >= period_end:
                continue
                
            # Ajustar os limites do agendamento para dentro do período
            adjusted_start = max(occupied_start, period_start)
            adjusted_end = min(occupied_end, period_end)
            
            # Se há tempo livre antes do agendamento
            if current_time < adjusted_start:
                free_intervals.append((current_time, adjusted_start))
            
            # Atualizar tempo atual para após o agendamento
            current_time = max(current_time, adjusted_end)
        
        # Se há tempo livre após o último agendamento
        if current_time < period_end:
            free_intervals.append((current_time, period_end))
            
        return free_intervals

    @classmethod
    def __adjust_intervals_to_full_hours(cls, intervals: List[tuple]) -> List[tuple]:
        """Ajusta os intervalos para começar e terminar apenas em horários cheios (sem minutos)"""
        
        adjusted_intervals = []
        
        for start, end in intervals:
            # Ajustar início para a próxima hora cheia se tiver minutos
            if start.minute > 0:
                adjusted_start = start.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            else:
                adjusted_start = start
            
            # Ajustar fim para a hora cheia anterior se tiver minutos
            if end.minute > 0:
                adjusted_end = end.replace(minute=0, second=0, microsecond=0)
            else:
                adjusted_end = end
            
            # Só adicionar se o intervalo ajustado ainda é válido (início antes do fim)
            if adjusted_start < adjusted_end:
                adjusted_intervals.append((adjusted_start, adjusted_end))
                
        return adjusted_intervals

    @classmethod
    def __format_available_intervals(cls, intervals: List[tuple]) -> str:
        """Formata os intervalos disponíveis para exibição"""
        
        if not intervals:
            return "Nenhum horário disponível no dia"
        
        formatted_intervals = []
        for start, end in intervals:
            start_str = start.strftime("%H:%M")
            end_str = end.strftime("%H:%M")
            formatted_intervals.append(f"{start_str} às {end_str}")
        
        return ", ".join(formatted_intervals)
    
    async def __register_schedule_informations(self, pet: ScheduleDTO) -> Dict:

        await self.__repository.create_schedule(pet)

        return {"mensagem": "Agendamento cadastrado com Sucesso"}