from abc import ABC, abstractmethod
from typing import List, Dict

class InterfaceGetAllPetsByCpfClient(ABC):

    @abstractmethod
    async def get_all_pets(self, cpf_client: str) -> List[Dict]: pass