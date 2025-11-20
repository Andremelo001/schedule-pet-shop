from uuid import UUID

class Client():
    def __init__(self, id: UUID, name: str, cpf: str, age: int, email: str, senha: str) -> None:
        self.id = id
        self.name = name
        self.cpf = cpf
        self.age = age
        self.email = email
        self.senha = senha