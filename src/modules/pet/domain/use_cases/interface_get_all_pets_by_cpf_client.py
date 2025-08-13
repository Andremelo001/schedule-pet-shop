from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import List, Dict

from src.modules.pet.domain.models.pet import Pet

class InterfaceGetAllPetsByCpfClient(ABC):

    @abstractmethod
    async def get_all_pets(self, session: AsyncSession, cpf_client: str) -> List[Dict]: pass