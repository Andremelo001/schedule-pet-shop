from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID

class PetDTO(SQLModel):
    id_client: UUID
    name: str
    breed: str
    age: int
    size_in_centimeters: int

class PetUpdateDTO(SQLModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    size_in_centimeters: Optional[str] = None