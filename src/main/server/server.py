from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.db.database import init_db
from src.main.routes import client_routes, pet_routes

# Configurações de inicialização do banco 
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# Inicializa o aplicativo FastAPI
app = FastAPI(lifespan=lifespan)

# Rotas para Endpoints
app.include_router(client_routes.router)
app.include_router(pet_routes.router)
