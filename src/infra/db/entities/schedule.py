from datetime import date, time
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

from src.infra.db.entities.services import Services
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infra.db.entities.client import Client, ClientBase
    from src.infra.db.entities.pet import Pet, PetBase
    


class ScheduleServices(SQLModel, table=True):
    services_id: UUID = Field(default=None, foreign_key="services.id", primary_key=True)
    schedule_id: UUID = Field(default=None, foreign_key="schedule.id", primary_key=True)


class ScheduleBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    date_schedule: date
    time_schedule: time
    total_price_schedule: int
    schedule_active: bool


class Schedule(ScheduleBase, table=True):
    client_id: UUID = Field(foreign_key="client.id")
    pet_id: UUID = Field(foreign_key="pet.id")
    client: "Client" = Relationship(back_populates="schedules")
    pet: "Pet" = Relationship(back_populates="schedules")
    services: list["Services"] = Relationship(link_model=ScheduleServices)


class ScheduleWithClientPetServices(ScheduleBase):
    client: "ClientBase"
    pet: "PetBase"
    services: list["Services"]
