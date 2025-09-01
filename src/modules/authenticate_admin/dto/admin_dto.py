from sqlmodel import SQLModel

class LoginRequest(SQLModel):
    senha: str
    user: str