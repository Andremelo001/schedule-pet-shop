from uuid import UUID

class Client():
    def __init(self, id: UUID, name: str, cpf: str, age: int, email: str, senha: str, is_admin: bool) -> None:
        self.id = id
        self.name = name
        self.cpf = cpf
        self.age = age
        self.email = email
        self.senha = senha
        self.is_admin = is_admin
    


