from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from typing import List

from src.modules.pet.data.interfaces.interface_pet_repository import InterfacePetRepository
from src.modules.pet.dto.pet_dto import PetDTO, PetUpdateDTO
from src.modules.pet.domain.models.pet import Pet
from src.infra.db.entities.pet import Pet as PetEntitie
from src.infra.db.entities.client import Client as ClientEntitie
from src.modules.user.domain.models.client import Client

class PetRepository(InterfacePetRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create_pet(self, id_client: str, pet: PetDTO) -> Pet:

        try: 
            new_pet = PetEntitie(
                id= uuid4(),
                name= pet.name,
                breed= pet.breed,
                age= pet.age,
                size_in_centimeters= pet.size_in_centimeters,
                client_id= id_client,
            )

            self.__session.add(new_pet)

            await self.__session.commit()

            await self.__session.refresh(new_pet)

        except Exception as exception:
            await self.__session.rollback()

            raise exception

    async def delete_pet(self, id_pet: str) -> None:

        pet_delete = await self.__session.execute(select(PetEntitie).where(PetEntitie.id == id_pet))

        await self.__session.delete(pet_delete.scalar_one_or_none())

        await self.__session.commit()

    async def uptdate_pet(self, id_pet: str, pet: PetUpdateDTO) -> Pet:

        statement = await self.__session.execute(select(PetEntitie).where(PetEntitie.id == id_pet))

        new_pet = statement.scalar_one_or_none()

        for key, value in pet.model_dump(exclude_unset=True).items():
            setattr(new_pet, key, value)

        await self.__session.commit()
        await self.__session.refresh(new_pet)

        return new_pet

    async def get_pet(self, id_pet: str) -> Pet:

        pet = await self.__session.execute(select(PetEntitie).where(PetEntitie.id == id_pet))

        return pet.scalar_one_or_none()

    async def get_all_pets_by_cpf_client(self, cpf_client: str) -> List[Pet]:

        pets_by_cpf_client = await self.__session.execute(select(PetEntitie)
        .join(ClientEntitie, PetEntitie.client_id == ClientEntitie.id)
        .where(ClientEntitie.cpf == cpf_client))

        return pets_by_cpf_client.scalars().all()

    async def get_name_pet_by_id_client(self, id_client: str) -> List[str]:

        statement = await self.__session.execute(select(PetEntitie.name).where(PetEntitie.client_id == id_client))

        names_pet = statement.scalars().all()

        return names_pet
    
    async def get_client_by_id(self, id_client: str) -> Client:

        client = await self.__session.execute(select(ClientEntitie).where(ClientEntitie.id == id_client))

        return client.scalar_one_or_none()

        