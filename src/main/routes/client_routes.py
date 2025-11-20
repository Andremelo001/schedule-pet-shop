from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

#import dtos from documentation Swagger
from src.modules.user.dto.client_dto import ClientDTO, ClientUpdateDTO

from src.modules.authenticate_user.dto.authenticate_user_dto import LoginRequest

from src.presentation.http_types.http_response import HttpResponse

from src.infra.db.settings.connection import DBConection

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.client_composers.client_create_composer import client_create_composer
from src.main.composers.client_composers.client_finder_composer import client_finder_composer
from src.main.composers.client_composers.client_update_composer import client_update_composer
from src.main.composers.client_composers.client_delete_composer import client_delete_composer
from src.main.composers.authenticate_user_composers.generate_token_composer import generate_token_composer
from src.main.composers.client_composers.get_client_with_pets_and_schedules_composer import get_client_with_pets_and_schedules_composer
from src.main.composers.client_composers.pay_schedule_composer import pay_schedule_composer
from src.main.composers.client_composers.process_payment_composer import process_payment_composer

#Import Middlewares
from src.middlewares.ensureAuthenticated import ensure_admin, ensure_client

db = DBConection()

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@router.post("/create", response_model=Dict, openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": ClientDTO.model_json_schema()
                }   
            }
        }
    })
async def create_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response: HttpResponse = await request_adapter(request, session, client_create_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)


@router.get("/find", response_model=Dict, openapi_extra={
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
async def get_client(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):


    http_response: HttpResponse = await request_adapter(request, session, client_finder_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.put("/update", response_model=Dict, openapi_extra={
        "security": [{"BearerAuth": []}],
        "parameters": [
            {
                "name": "id_client",
                "in": "query",
                "required": True,
                "schema": {"type": "string"},
            }
        ],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": ClientUpdateDTO.model_json_schema()
                }   
            }
        }
    })
async def update_client(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response: HttpResponse = await request_adapter(request, session, client_update_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.delete("/delete", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "id_client",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
        }
    ]
})
async def delete_client(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response: HttpResponse = await request_adapter(request, session, client_delete_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.post("/login", response_model=Dict, openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": LoginRequest.model_json_schema()
                }   
            }
        }
    })
async def login_client(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response: HttpResponse = await request_adapter(request, session, generate_token_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/get_client_with_pets_and_schedules", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "id_client",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
        }
    ]
})
async def get_client_with_pets_and_schedules(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response: HttpResponse = await request_adapter(request, session, get_client_with_pets_and_schedules_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/pay_schedule", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "id_schedule",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
        }
    ]
    
})
async def pay_schedule(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response: HttpResponse = await request_adapter(request, session, pay_schedule_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.post("/notification", response_model=Dict)
async def receive_notification(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response: HttpResponse = await request_adapter(request, session, process_payment_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)


