from abc import ABC, abstractmethod
from src.presentation.http_types.http_response import HttpResponse

class MessageControllerInterface(ABC):

    @abstractmethod
    async def handle(self, message_body: dict) -> HttpResponse: pass