import jwt
from datetime import datetime, timedelta
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
JWT_EXPIRATION = int(config('JWT_EXPIRATION'))

class JWTService:

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now() + timedelta(minutes=JWT_EXPIRATION)

        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def validate_token(self, token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])




