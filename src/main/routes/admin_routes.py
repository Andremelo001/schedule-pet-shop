from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.infra.db.settings.connection import DBConection

#import dtos from documentation Swagger
from src.modules.authenticate_admin.dto.admin_dto import LoginRequest

from src.presentation.http_types.http_response import HttpResponse

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.authenticate_admin_composers.generate_token_admin_composer import generate_token_admin_composer

db = DBConection()

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.post("/login", response_model=Dict, openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": LoginRequest.model_json_schema()
                }   
            }
        }
    })
async def login_admin(request: Request, session: AsyncSession = Depends(db.get_session)):

    http_response: HttpResponse = await request_adapter(request, session, generate_token_admin_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)