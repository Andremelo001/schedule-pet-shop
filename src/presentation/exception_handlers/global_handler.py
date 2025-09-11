from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.errors.error_handler import handle_errors
from src.presentation.http_types.http_response import HttpResponse

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        http_response: HttpResponse = handle_errors(exc)
        
        return JSONResponse(
            status_code=http_response.status_code,
            content=http_response.body
        )
