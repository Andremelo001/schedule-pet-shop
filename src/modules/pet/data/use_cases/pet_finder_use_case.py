from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.pet.data.interfaces.interface_pet_repository import InterfacePetRepository
from src.modules.pet.domain.use_cases.interface_pet_finder import InterfaceFinderPet
from src.modules.pet.domain.models.pet import Pet
from typing import Dict

from src.errors.error_handler import HttpNotFoundError

class PetFinderUseCase(InterfaceFinderPet):
    def __init__(self, repository: InterfacePetRepository):
        self.repository = repository

    async def finder(self, session: AsyncSession, id_pet: str) -> Dict:

        pet = await self.repository.get_pet(session, id_pet)

        if not pet:
            raise HttpNotFoundError(f"Pet com o id {id_pet} não encontrado")
        
        return self.__format_response(pet)

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


    