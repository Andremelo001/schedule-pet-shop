from uuid import UUID

class Admin():
    def __init__(self, id_admin: UUID, senha: str, user: str, name: str):
        self.id_admin = id_admin
        self.senha = senha
        self.user = user
        self.name = name