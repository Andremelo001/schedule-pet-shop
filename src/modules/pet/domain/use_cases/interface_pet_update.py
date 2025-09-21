from abc import ABC, abstractmethod
from src.modules.pet.dto.pet_dto import PetUpdateDTO
from src.modules.pet.domain.models.pet import Pet


class InterfacePetUpdate(ABC):

    @abstractmethod
    async def update(self, id_client: str, id_pet: str, pet: PetUpdateDTO) -> Pet: pass