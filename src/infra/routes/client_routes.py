from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db.settings.connection import DBConection
from src.infra.db.entities.client import Client
from src.infra.dtos.client_dto import CreateClient
from src.infra.db.repositories.client_repository import ClientRepository

db = DBConection()

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@router.post("/", response_model=Client)
async def create_client(client: CreateClient, session: AsyncSession = Depends(db.get_session)):
    client_exist = await ClientRepository.client_exists(session, client.cpf)

    if client_exist:
        raise HTTPException(status_code=400, detail=f"Cliente com o cpf {client.cpf} já foi cadastrado")

    return await ClientRepository.create_client(session, client)
