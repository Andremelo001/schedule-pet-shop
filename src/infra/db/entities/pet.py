from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infra.db.entities.client import Client
    from src.infra.db.entities.schedule import Schedule


class PetBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    breed: str
    age: int
    size_in_centimeters: int


class Pet(PetBase, table=True):
    client_id: UUID = Field(foreign_key="client.id", ondelete="CASCADE")
    client: "Client" = Relationship(back_populates="pets")
    schedules: list["Schedule"] = Relationship(back_populates="pet", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
