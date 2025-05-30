from sqlmodel import SQLModel
from typing import Optional

class ClientDTO(SQLModel):
    name: str
    cpf: str
    age: int
    email:str
    senha: str

class ClientUpdateDTO(SQLModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    senha: Optional[str] = None