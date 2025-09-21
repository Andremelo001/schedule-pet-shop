from typing import Dict, List

from src.modules.pet.domain.use_cases.interface_get_all_pets_by_cpf_client import InterfaceGetAllPetsByCpfClient
from src.modules.pet.data.interfaces.interface_pet_repository import InterfacePetRepository
from src.modules.pet.domain.models.pet import Pet

from src.errors.types_errors import HttpNotFoundError

class GetAllPetsByCpfClientUseCase(InterfaceGetAllPetsByCpfClient):
    def __init__(self, repository: InterfacePetRepository):
        self.__repository = repository

    async def get_all_pets(self, cpf_client: str) -> List[Dict]:

        pets = await self.__repository.get_all_pets_by_cpf_client(cpf_client)

        if not pets:
            raise HttpNotFoundError("Pets do cliente não encontrados")

        return self.__format_response(pets)

    @classmethod
    def __format_response(cls, pets: List[Pet]) -> List[Dict]:

        return [{
            "id": str(pet.id),
            "name": pet.name,
            "breed": pet.breed,
            "age": pet.age,
            "size_in_centimeters": pet.size_in_centimeters,
            "client_id": str(pet.client_id)
        } for pet in pets]