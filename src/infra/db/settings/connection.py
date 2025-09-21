from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 
from typing import AsyncGenerator

class DBConection:

    def __init__(self):

        # Carregar variáveis do .env
        load_dotenv()

        self.__database_url = os.getenv("DATABASE_URL")

        self.__engine = self.__create_engine()

        self.__async_session_maker = self.__create_session()
    

    # Criar motor assíncrono
    def __create_engine(self):
        return create_async_engine(self.__database_url, echo=True)

    # Criar fábrica de sessões assíncronas
    def __create_session(self):
        return sessionmaker(self.__engine, class_=AsyncSession, expire_on_commit=False)

    # Dependência para obter uma sessão assíncrona
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__async_session_maker() as session:
            yield session
    
    @property
    def engine(self):
        return self.__engine

    

