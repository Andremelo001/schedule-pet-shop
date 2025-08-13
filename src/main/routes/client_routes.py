from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.client_composers.client_create_composer import client_create_composer
from src.main.composers.client_composers.client_finder_composer import client_finder_composer
from src.main.composers.client_composers.client_update_composer import client_update_composer
from src.main.composers.client_composers.client_delete_composer import client_delete_composer
from src.main.composers.authenticate_user_composers.generate_token_composer import generate_token_composer

#Import Error Handler
from src.errors.error_handler import handle_errors

db = DBConection()

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@router.post("/create", response_model=Dict)
async def create_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, client_create_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)


@router.get("/find", response_model=Dict)
async def get_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, client_finder_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.put("/update", response_model=Dict)
async def update_client(
    request: Request, session: AsyncSession = Depends(db.get_session)
    ):

    http_response = None

    try:
        http_response = await request_adapter(request, session, client_update_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.delete("/delete", response_model=Dict)
async def delete_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, client_delete_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.post("/login", response_model=Dict)
async def login_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, generate_token_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)


