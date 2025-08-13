from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.modules.pet.domain.use_cases.interface_pet_create import InterfacePetCreate
from src.modules.pet.data.interfaces.interface_pet_repository import InterfacePetRepository
from src.modules.pet.dto.pet_dto import PetDTO

from src.errors.types_errors import HttpConflitError

class PetCreateUseCase(InterfacePetCreate):
    def __init__(self, repository: InterfacePetRepository):
        self.repository = repository

    async def create(self, session: AsyncSession, pet: PetDTO, id_client: str) -> Dict:

        await self.__verify_name_exists(session, id_client, pet.name)

        return await self.__register_pet_informations(session, id_client, pet)

    async def __verify_name_exists(self, session: AsyncSession, id_client: str, pet_name: str) -> None:

        names_pet = await self.repository.get_name_pet_by_id_client(session, id_client)

        if pet_name in names_pet:
            raise HttpConflitError(f"Cliente com o id {id_client}, já tem um pet cadastrado com o nome {pet_name}")
    
    async def __register_pet_informations(self, session: AsyncSession, id_client: str, pet: PetDTO) -> Dict:

        await self.repository.create_pet(session, id_client, pet)

        return {"message": "Pet cadastrado com sucesso"}