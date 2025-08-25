from sqlmodel import SQLModel

class ServiceDTO(SQLModel):
    duration_in_minutes: int
    type_service: str
    price: float