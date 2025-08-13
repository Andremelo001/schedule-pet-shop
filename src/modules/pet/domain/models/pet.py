from uuid import UUID

class Pet():
    def __init__(self, id: UUID, name: str, breed: str, age: int, size_in_centimeters: int, client_id: UUID) -> None:
        self.id = id
        self.name = name
        self.breed = breed
        self.age = age
        self.size_in_centimeters = size_in_centimeters
        self.client_id = client_id