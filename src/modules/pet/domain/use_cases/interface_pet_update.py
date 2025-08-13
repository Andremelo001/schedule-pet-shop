from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.pet.dto.pet_dto import PetUpdateDTO
from src.modules.pet.domain.models.pet import Pet


class InterfacePetUpdate(ABC):

    @abstractmethod
    async def update(self, session: AsyncSession, id_client: str, id_pet: str, pet: PetUpdateDTO) -> Pet: pass