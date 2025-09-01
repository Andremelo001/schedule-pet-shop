from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection

#import dtos from documentation Swagger
from src.modules.schedule.dto.schedule_dto import ScheduleDTO

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.schedule_composers.schedule_create_composer import schedule_create_composer
from src.main.composers.schedule_composers.request_cancel_schedule_composer import request_cancel_schedule
from src.main.composers.schedule_composers.cancel_schedule_composer import cancel_schedule
from src.main.composers.schedule_composers.schedule_delete_composer import schedule_delete_composer
from src.main.composers.schedule_composers.schedule_list_composer import schedule_list_composer
from src.main.composers.schedule_composers.find_schedules_actives_composer import find_schedules_actives_composer

#Import Error Handler
from src.errors.error_handler import handle_errors

#Import Middlewares
from src.middlewares.ensureAuthenticated import ensure_client, ensure_delete_schedule, ensure_admin

db = DBConection()

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"],
)

@router.post("/create", response_model=Dict, openapi_extra={
        "security": [{"BearerAuth": []}],
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": ScheduleDTO.model_json_schema()
                }   
            }
        }
    })
async def create_schedule(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, schedule_create_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.post("/request_cancel_schedule", response_model=Dict, openapi_extra={
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
async def request_cancel(request: Request, session: AsyncSession = Depends(db.get_session), ensureClient = Depends(ensure_client)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, request_cancel_schedule)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.post("/cancel_schedule", response_model=Dict, openapi_extra={
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
async def cancel(request: Request, session: AsyncSession = Depends(db.get_session), ensureDeleteSchedule = Depends(ensure_delete_schedule)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, cancel_schedule)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.delete("/delete", response_model=Dict, openapi_extra={
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
async def delete(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, schedule_delete_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/list", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}]
})
async def list(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, schedule_list_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)

@router.get("/list_schedules_actives", response_model=Dict, openapi_extra={
    "security": [{"BearerAuth": []}]
})
async def list_schedules_actives(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, find_schedules_actives_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)