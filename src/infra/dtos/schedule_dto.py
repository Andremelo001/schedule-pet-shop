from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime

class CreateSchedule(SQLModel):
    date_schedule: datetime
    client_id: UUID
    pet_id: UUID
    services_ids: list[UUID]

class UpdateSchedule(SQLModel):
    date_schedule: datetime | None