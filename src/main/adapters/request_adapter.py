from typing import Callable
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
import json

from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

async def request_adapter(request: Request, session: AsyncSession, controller: Callable) -> HttpResponse:

    try:
        body = await request.json() if await request.body() else {}
    except json.decoder.JSONDecodeError:
        body = {}

    http_request = HttpRequest(
        headers=dict(request.headers),
        body=body,
        query_params=dict(request.query_params),
        path_params=dict(request.path_params),
        url=str(request.url)
    )

    http_response = await controller(session, http_request)

    return http_response