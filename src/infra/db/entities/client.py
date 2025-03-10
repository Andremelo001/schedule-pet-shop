from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from src.infra.db.entities.pet import Pet, PetBase
from src.infra.db.entities.schedule import Schedule


class ClientBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    cpf: str = Field(unique=True)
    age: int
    email: str
    senha: str
    is_admin: bool = Field(default=False)


class Client(ClientBase, table=True):
    pets: list["Pet"] = Relationship(back_populates="client")
    schedules: list["Schedule"] = Relationship(back_populates="client")


class ClientBaseWithPets(ClientBase):
    pets: list["PetBase"] = []
