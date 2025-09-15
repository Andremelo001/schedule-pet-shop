from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import List, Dict

class InterfaceGetAllPetsByCpfClient(ABC):

    @abstractmethod
    async def get_all_pets(self, session: AsyncSession, cpf_client: str) -> List[Dict]: pass