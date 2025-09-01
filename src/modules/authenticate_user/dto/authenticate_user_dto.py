from sqlmodel import SQLModel

class LoginRequest(SQLModel):
    email:str
    senha: str