from sqlmodel import SQLModel
from typing import List
from datetime import date, time

class ScheduleDTO(SQLModel):
    date_schedule: date
    time_schedule: time
    id_client: str
    id_pet: str
    list_services: List[str]