from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import List

from src.modules.pet.domain.models.pet import Pet
from src.modules.pet.dto.pet_dto import PetDTO, PetUpdateDTO

class InterfacePetRepository(ABC):

    @abstractmethod
    async def create_pet(cls, session: AsyncSession, id_client: str, pet: PetDTO) -> Pet: pass

    @abstractmethod
    async def delete_pet(cls, session: AsyncSession, id_pet: str) -> None: pass

    @abstractmethod
    async def uptdate_pet(cls, session: AsyncSession, id_pet: str, pet: PetUpdateDTO) -> Pet: pass

    @abstractmethod
    async def get_pet(cls, session: AsyncSession, id_pet: str) -> Pet: pass

    @abstractmethod
    async def get_all_pets_by_cpf_client(cls, session: AsyncSession, cpf_client: str) -> List[Pet]: pass

    @abstractmethod
    async def get_name_pet_by_id_client(cls, session: AsyncSession, id_client: str) -> List[str]: pass

    
