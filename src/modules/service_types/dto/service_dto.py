from sqlmodel import SQLModel
from typing import Optional

class ServiceDTO(SQLModel):
    duration_in_minutes: int
    type_service: str
    price: float

class UpdateServiceDTO(SQLModel):
    duration_in_minutes: Optional[int] = None
    type_service: Optional[str] = None
    price: Optional[float] = None
