from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from src.modules.user.data.interfaces.interface_client_repository import InterfaceClientRepository
from src.modules.user.domain.use_cases.interface_client_delete import InterfaceClientDelete

class ClientDeleteUseCase(InterfaceClientDelete):
    def __init__(self, repositoy: InterfaceClientRepository):
        self.repository = repositoy

    async def delete(self, session: AsyncSession, id_client: str) -> Dict:

        await self.repository.delete_client(session, id_client)

        return {"message": "Cliente deletado com sucesso do banco de dados"}
