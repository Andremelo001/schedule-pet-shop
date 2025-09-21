from abc import ABC, abstractmethod
from typing import List

from src.modules.user.domain.models.client import Client
from src.infra.db.entities.client import ClientWithPetsWithSchedules
from src.modules.user.dto.client_dto import ClientDTO, ClientUpdateDTO
from src.modules.schedule.domain.models.schedule import Schedule

class InterfaceClientRepository(ABC):

    @abstractmethod
    async def get_client_by_id(self, id_client: str) -> Client: pass

    @abstractmethod
    async def get_client_with_pets_and_schedules_by_id(self, id_client: str) -> ClientWithPetsWithSchedules: pass

    @abstractmethod
    async def get_client(self, cpf_client: str) -> Client: pass

    @abstractmethod
    async def get_client_by_email(self, email: str) -> Client: pass

    @abstractmethod
    async def create_client(self, client: ClientDTO) -> Client: pass

    @abstractmethod
    async def update_client(self, id_client: str, client: ClientUpdateDTO) -> Client: pass

    @abstractmethod
    async def delete_client(self, id_client: str) -> None: pass

    @abstractmethod
    async def find_schedule_by_id_client(self, id_client: str) -> List[Schedule]: pass

        



