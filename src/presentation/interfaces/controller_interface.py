from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class ControllerInterface(ABC):

    @abstractmethod
    async def handle(self, session: AsyncSession, http_request: HttpRequest) -> HttpResponse: pass


