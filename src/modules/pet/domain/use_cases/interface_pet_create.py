from abc import ABC, abstractmethod
from typing import Dict

from src.modules.pet.dto.pet_dto import PetDTO

class InterfacePetCreate(ABC):

    @abstractmethod
    async def create(self, pet: PetDTO, id_client: str ) -> Dict: pass