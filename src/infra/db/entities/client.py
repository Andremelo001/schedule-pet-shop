from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from src.infra.db.entities.pet import Pet, PetBase
from src.infra.db.entities.schedule import Schedule, ScheduleBase


class ClientBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    cpf: str = Field(unique=True)
    age: int
    email: str
    senha: str


class Client(ClientBase, table=True):
    pets: list["Pet"] = Relationship(back_populates="client", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    schedules: list["Schedule"] = Relationship(back_populates="client", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ClientWithPetsWithSchedules(ClientBase):
    pets: list["PetBase"] = []
    schedules: list["ScheduleBase"] = []
