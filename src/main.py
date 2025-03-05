from fastapi import FastAPI
from contextlib import asynccontextmanager
from .infra.db.database import init_db

# Configurações de inicialização
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# Inicializa o aplicativo FastAPI
app = FastAPI(lifespan=lifespan)

# Rotas para Endpoints
