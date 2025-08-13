from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from src.modules.pet.domain.use_cases.interface_pet_delete import InterfacePetDelete
from src.modules.pet.data.interfaces.interface_pet_repository import InterfacePetRepository

from src.errors.error_handler import HttpNotFoundError

class PetDeleteUseCase(InterfacePetDelete):
    def __init__(self, repository: InterfacePetRepository):
        self.repository = repository

    async def delete(self, session: AsyncSession, id_pet: str) -> Dict:

        await self.__pet_exists(session, id_pet)

        await self.repository.delete_pet(session, id_pet)

        return {"message": "Pet deletado com sucesso do banco de dados"}
    
    async def __pet_exists(self, session: AsyncSession, id_pet: str) -> None:

        pet = await self.repository.get_pet(session, id_pet)

        if not pet:
            raise HttpNotFoundError(f"Pet com o id {id_pet} não encontrado")