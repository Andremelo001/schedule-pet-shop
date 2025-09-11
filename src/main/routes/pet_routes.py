from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from src.infra.db.settings.connection import DBConection

#import dtos from documentation Swagger
from src.modules.pet.dto.pet_dto import PetDTO, PetUpdateDTO

from src.presentation.http_types.http_response import HttpResponse

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

from src.main.composers.pet_composers.pet_create_composer import pet_create_composer
from src.main.composers.pet_composers.pet_delete_composer import pet_delete_composer
from src.main.composers.pet_composers.get_all_pets_composer import get_all_pets_composer
from src.main.composers.pet_composers.pet_finder_composer import pet_finder_composer
from src.main.composers.pet_composers.pet_update_composer import pet_update_composer

#Import Middlewares
from src.middlewares.ensureAuthenticated import ensure_client

db = DBConection()

router = APIRouter(
    prefix="/pets",
    tags=["Pets"],
)

@router.post("/create", response_model=Dict, openapi_extra={
        "security": [{"BearerAuth": []}],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": PetDTO.model_json_schema()
                }   
            }
        }
    })
async def create_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response: HttpResponse = await request_adapter(request, session, pet_create_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/get_all_pets", response_model=List[Dict], openapi_extra={
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "cpf_client",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
        }
    ]
})
async def list_pets(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response: HttpResponse = await request_adapter(request, session, get_all_pets_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/finder", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "id_pet",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
        }
    ]
})
async def finder_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response: HttpResponse = await request_adapter(request, session, pet_finder_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.delete("/delete", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "id_pet",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
        }
    ]
})
async def delete_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response: HttpResponse = await request_adapter(request, session, pet_delete_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.put("/update", response_model=Dict, openapi_extra={
        "security": [{"BearerAuth": []}],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": PetUpdateDTO.model_json_schema()
                }   
            }
        }
    })
async def update_pet(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response: HttpResponse = await request_adapter(request, session, pet_update_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)