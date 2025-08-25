from uuid import UUID

class Service():
    def __init__(self, id: UUID, duration_in_minutes: int, type_service: str, price: float) -> None:
        self.id = id
        self.duration_in_minutes = duration_in_minutes
        self.type_service = type_service
        self.price = price