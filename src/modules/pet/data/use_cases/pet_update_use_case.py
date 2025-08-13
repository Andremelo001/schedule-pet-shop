from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.pet.data.interfaces.interface_pet_repository import InterfacePetRepository
from src.modules.pet.dto.pet_dto import PetUpdateDTO
from src.modules.pet.domain.models.pet import Pet
from src.modules.pet.domain.use_cases.interface_pet_update import InterfacePetUpdate

from typing import Dict

from src.errors.error_handler import HttpConflitError


class PetUpdateUseCase(InterfacePetUpdate):
    def __init__(self, repository: InterfacePetRepository):
        self.repository = repository

    async def update(self, session: AsyncSession, id_client: str, id_pet: str, pet: PetUpdateDTO) -> Dict:

        await self.__pet_exists(session, pet.name, id_client)

        new_pet = await self.repository.uptdate_pet(session, id_pet, pet)

        return self.__format_response(new_pet)
    
    async def __pet_exists(self, session: AsyncSession, pet_name: str, id_client: str) -> None:

        names_pet = await self.repository.get_name_pet_by_id_client(session, id_client)

        if pet_name in names_pet:
            raise HttpConflitError(f"Pet com o nome {pet_name} já existe")
    
    @classmethod
    def __format_response(cls, pet: Pet) -> Dict:

        return {
            "id": str(pet.id),
            "name": pet.name,
            "breed": pet.breed,
            "age": pet.age,
            "size_in_centimeters": pet.size_in_centimeters,
            "client_id": str(pet.client_id)
        }