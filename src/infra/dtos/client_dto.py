from sqlmodel import SQLModel

class CreateClient(SQLModel):
    name: str
    cpf: str
    age: int
    email: str
    senha: str

class UpdateCliente(SQLModel):
    name: str | None
    cpf: str | None
    age: str | None