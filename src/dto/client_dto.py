from sqlmodel import SQLModel

class ClientDTO(SQLModel):
    name: str
    cpf: str
    age: int
    email:str
    senha: str