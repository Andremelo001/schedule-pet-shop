from typing import Dict
from src.modules.pet.domain.use_cases.interface_pet_create import InterfacePetCreate
from src.modules.pet.data.interfaces.interface_pet_repository import InterfacePetRepository
from src.modules.pet.dto.pet_dto import PetDTO
from src.errors.types_errors import HttpConflitError, HttpNotFoundError

class PetCreateUseCase(InterfacePetCreate):
    def __init__(self, repository: InterfacePetRepository):
        self.__repository = repository

    async def create(self, pet: PetDTO, id_client: str) -> Dict:

        await self.__client_not_found(id_client)

        await self.__verify_name_exists(id_client, pet.name)

        return await self.__register_pet_informations(id_client, pet)

    async def __verify_name_exists(self, id_client: str, pet_name: str) -> None:

        names_pet = await self.__repository.get_name_pet_by_id_client(id_client)

        if pet_name in names_pet:
            raise HttpConflitError(f"Cliente com o id {id_client}, já tem um pet cadastrado com o nome {pet_name}")
        
    async def __client_not_found(self, id_client: str):

        client = await self.__repository.get_client_by_id(id_client)

        if not client:
            raise HttpNotFoundError(f"Cliente com o id {id_client} não encontrado")
    
    async def __register_pet_informations(self, id_client: str, pet: PetDTO) -> Dict:

        await self.__repository.create_pet(id_client, pet)

        return {"message": "Pet cadastrado com sucesso"}