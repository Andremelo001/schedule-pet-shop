from fastapi import Request
from src.errors.types_errors import HttpUnauthorized
from src.drivers.jwt.jwt_service import JWTService

jwt_service = JWTService()

async def ensureAuthenticated(request: Request):

    authorization = request.headers.get("Authorization")
    
    if not authorization:
        raise HttpUnauthorized("Token missing")
    
    try:
        token = authorization.split(" ")[1]

        payload = jwt_service.validate_token(token)

        return payload
    
    except Exception:
        raise HttpUnauthorized("Invalid token")


