from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Services(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    duration_in_minutes: int
    type_service: str
    price: float
