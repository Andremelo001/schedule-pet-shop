from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from src.infra.db.settings.connection import DBConection

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

from src.main.composers.pet_composers.pet_create_composer import pet_create_composer
from src.main.composers.pet_composers.pet_delete_composer import pet_delete_composer
from src.main.composers.pet_composers.get_all_pets_composer import get_all_pets_composer
from src.main.composers.pet_composers.pet_finder_composer import pet_finder_composer
from src.main.composers.pet_composers.pet_update_composer import pet_update_composer

#Import Error Handler
from src.errors.error_handler import handle_errors

#Import Middlewares
from src.middlewares.ensureAuthenticated import ensureAuthenticated

db = DBConection()

router = APIRouter(
    prefix="/pets",
    tags=["Pets"],
)

@router.post("/create", response_model=Dict)
async def create_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureAuthenticated = Depends(ensureAuthenticated)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, pet_create_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/get_all_pets", response_model=List[Dict])
async def list_pets(request: Request, session: AsyncSession = Depends(db.get_session), ensureAuthenticated = Depends(ensureAuthenticated)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, get_all_pets_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/finder", response_model=Dict)
async def finder_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureAuthenticated = Depends(ensureAuthenticated)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, pet_finder_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.delete("/delete", response_model=Dict)
async def delete_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureAuthenticated = Depends(ensureAuthenticated)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, pet_delete_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.put("/update", response_model=Dict)
async def update_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureAuthenticated = Depends(ensureAuthenticated)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, pet_update_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)