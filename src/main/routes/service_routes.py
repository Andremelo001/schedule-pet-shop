from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.service_composers.service_create_composer import service_create_composer

#Import Error Handler
from src.errors.error_handler import handle_errors

#Import Middlewares
from src.middlewares.ensureAuthenticated import ensure_admin

db = DBConection()

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)

@router.post("/create", response_model=Dict)
async def create_service(request: Request, session: AsyncSession = Depends(db.get_session), ensureAdmin = Depends(ensure_admin)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, service_create_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)