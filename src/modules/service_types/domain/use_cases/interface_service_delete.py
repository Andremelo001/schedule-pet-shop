from abc import ABC, abstractmethod

class InterfaceServiceDelete(ABC):

    @abstractmethod
    async def delete(self, id_service: str) -> None: pass