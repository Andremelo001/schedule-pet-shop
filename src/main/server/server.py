from fastapi import FastAPI
from src.infra.docs.openapi import custom_openapi
from contextlib import asynccontextmanager
from src.infra.db.database import init_db
from src.main.routes import client_routes, pet_routes, admin_routes, schedule_routes, service_routes

from src.presentation.exception_handlers.global_handler import register_exception_handlers

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
app.include_router(admin_routes.router)
app.include_router(schedule_routes.router)
app.include_router(service_routes.router)

register_exception_handlers(app)

app.openapi = lambda: custom_openapi(app)