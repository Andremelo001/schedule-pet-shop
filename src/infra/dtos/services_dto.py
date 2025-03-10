from sqlmodel import SQLModel

class CreateServices(SQLModel):
    duration_in_minutes: int
    type_service: str
    price: float

class UpdateServices(SQLModel):
    duration_in_minutes: int | None
    type_service: str | None
    price: float | None