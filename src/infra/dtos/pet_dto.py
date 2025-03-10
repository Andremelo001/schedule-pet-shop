from sqlmodel import SQLModel
from uuid import UUID

class CreatPet(SQLModel):
    name: str
    breed: str
    age: int
    size_in_centimeters: int
    id_client: UUID

class UpdatePet(SQLModel):
    name: str | None
    breed: str | None
    age: int | None
    size_in_centimeters: int | None