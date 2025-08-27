from uuid import UUID
from datetime import date, time
from typing import List

class Schedule():
    def __init__(self, id: UUID, date_schedule: date, time_schedule: time, client_id: UUID, pet_id: UUID, total_price_schedule: int, schedule_active: bool, services: List[UUID]) -> None:
        self.id = id
        self.date_schedule = date_schedule
        self.time_schedule = time_schedule
        self.client_id = client_id
        self.pet_id = pet_id
        self.total_price_schedule = total_price_schedule
        self.schedule_active = schedule_active
        self.services = services