from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.authenticate_admin_composers.generate_token_admin_composer import generate_token_admin_composer

#Import Error Handler
from src.errors.error_handler import handle_errors

db = DBConection()

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.post("/login", response_model=Dict)
async def login_admin(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response = None

    try:
        http_response = await request_adapter(request, session, generate_token_admin_composer)
    except Exception as exception:
        http_response = handle_errors(exception)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)