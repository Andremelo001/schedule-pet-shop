from abc import ABC, abstractmethod
from typing import List

from src.modules.pet.domain.models.pet import Pet
from src.modules.pet.dto.pet_dto import PetDTO, PetUpdateDTO
from src.modules.user.domain.models.client import Client

class InterfacePetRepository(ABC):

    @abstractmethod
    async def create_pet(self, id_client: str, pet: PetDTO) -> Pet: pass

    @abstractmethod
    async def delete_pet(self, id_pet: str) -> None: pass

    @abstractmethod
    async def uptdate_pet(self, id_pet: str, pet: PetUpdateDTO) -> Pet: pass

    @abstractmethod
    async def get_pet(self, id_pet: str) -> Pet: pass

    @abstractmethod
    async def get_all_pets_by_cpf_client(self, cpf_client: str) -> List[Pet]: pass

    @abstractmethod
    async def get_name_pet_by_id_client(self, id_client: str) -> List[str]: pass

    @abstractmethod
    async def get_client_by_id(self, id_client: str) -> Client: pass

    
