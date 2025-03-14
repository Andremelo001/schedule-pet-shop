from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection
from src.infra.db.entities.client import Client
from src.data.use_cases.client_create_use_case import CreateClientUseCase
from src.data.use_cases.client_finder_use_case import ClientFinderUseCase
from src.infra.db.repositories.client_repository import ClientRepository
from src.dto.client_dto import ClientDTO


db = DBConection()

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@router.post("/", response_model=Dict)
async def create_client(client: ClientDTO, session: AsyncSession = Depends(db.get_session)):

    client_service = CreateClientUseCase(ClientRepository)

    return await client_service.create(session, client)

@router.get("/", response_model=Client)
async def get_client(cpf_client: str, session: AsyncSession = Depends(db.get_session)):

    client_service = ClientFinderUseCase(ClientRepository)

    return await client_service.find(session, cpf_client)

