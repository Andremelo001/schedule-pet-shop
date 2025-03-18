from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection
from src.infra.db.entities.client import Client

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.client_create_composer import client_create_composer
from src.main.composers.client_finder_composer import client_finder_composer


db = DBConection()

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@router.post("/", response_model=Dict)
async def create_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response = await request_adapter(request, session, client_create_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)


@router.get("/", response_model=Dict)
async def get_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response = await request_adapter(request, session, client_finder_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)


