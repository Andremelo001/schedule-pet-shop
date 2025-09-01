from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection

#import dtos from documentation Swagger
from src.modules.service_types.dto.service_dto import ServiceDTO, UpdateServiceDTO

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.service_composers.service_create_composer import service_create_composer
from src.main.composers.service_composers.service_list_composer import service_list_composer
from src.main.composers.service_composers.service_delete_composer import service_delete_composer
from src.main.composers.service_composers.service_update_composer import service_update_composer

#Import Error Handler
from src.errors.error_handler import handle_errors

#Import Middlewares
from src.middlewares.ensureAuthenticated import ensure_admin

db = DBConection()

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)

@router.post("/create", response_model=Dict, openapi_extra={
        "security": [{"BearerAuth": []}],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": ServiceDTO.model_json_schema()
                }   
            }
        }
    })
async def create_service(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, service_create_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/list", response_model=Dict, openapi_extra={
        "security": [{"BearerAuth": []}]
    })
async def create_service(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, service_list_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.delete("/delete", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "id_service",
            "in": "query",
            "required": True,
            "schema": {"type": "string"},
        }
    ]
})
async def delete_service(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, service_delete_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.put("/update", response_model=Dict, openapi_extra={
        "security": [{"BearerAuth": []}],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": UpdateServiceDTO.model_json_schema()
                }   
            }
        }
    })
async def update_service(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, service_update_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)