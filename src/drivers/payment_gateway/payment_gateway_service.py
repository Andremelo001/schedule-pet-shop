from src.drivers.payment_gateway.interfaces.interface_payment_gateway import InterfacePaymentGateway
from typing import Dict
import httpx
from dotenv import load_dotenv
import os
import asyncio
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class PaymentGatewayService(InterfacePaymentGateway):
    def __init__(self):
        self.__base_url = (
            os.getenv("MICROSERVICE_URL_PRODUCTION") or 
            os.getenv("MICROSERVICE_URL_DEVELOPMENT")
        )
        self.__payment_endpoint = f"{self.__base_url}/payments/generate_payment"
        self.__get_payment_endpoint = f"{self.__base_url}/payments/finder_payment"
        self.__max_retries = 3
        self.__base_delay = 1.0
        self.__timeout = 60.0

    async def __retry_with_backoff(self, func, *args, **kwargs):
        """
        Implementa retry com backoff exponencial para lidar com rate limiting
        """
        for attempt in range(self.__max_retries):
            try:
                return await func(*args, **kwargs)
            
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    if attempt < self.__max_retries - 1:
                        # Calcula o delay com backoff exponencial
                        delay = self.__base_delay * (2 ** attempt)
                        
                        # Verifica se há header Retry-After
                        retry_after = e.response.headers.get("Retry-After")
                        if retry_after:
                            try:
                                delay = float(retry_after)
                            except ValueError:
                                pass
                        
                        logger.warning(
                            f"Rate limit atingido. Tentativa {attempt + 1}/{self.__max_retries}. "
                            f"Aguardando {delay}s..."
                        )
                        await asyncio.sleep(delay)
                        continue
                    else:
                        raise Exception(
                            f"Limite de requisições excedido. Por favor, tente novamente mais tarde. "
                            f"A API está temporariamente indisponível devido ao alto volume de requisições."
                        )
                else:
                    raise
                    
            except httpx.HTTPError as e:
                if attempt < self.__max_retries - 1:
                    delay = self.__base_delay * (2 ** attempt)
                    logger.warning(
                        f"Erro na requisição. Tentativa {attempt + 1}/{self.__max_retries}. "
                        f"Aguardando {delay}s..."
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise

    async def generate_payment(self, payment_info: Dict) -> Dict:
        async def _make_request():
            async with httpx.AsyncClient(timeout=self.__timeout) as client:
                response = await client.post(
                    self.__payment_endpoint,
                    json=payment_info
                )
                response.raise_for_status()
                return response.json()

        try:
            return await self.__retry_with_backoff(_make_request)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise Exception(
                    "Serviço de pagamentos temporariamente indisponível devido ao alto volume de requisições. "
                    "Por favor, tente novamente em alguns instantes."
                )
            raise Exception(f"Erro ao processar pagamento: {e.response.status_code} - {e.response.text}")
        except httpx.HTTPError as e:
            raise Exception(f"Erro ao comunicar com o microserviço de pagamentos: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao processar pagamento: {str(e)}")

    async def get_payment(self, id_schedule: str) -> Dict:
        async def _make_request():
            async with httpx.AsyncClient(timeout=self.__timeout) as client:
                response = await client.get(
                    self.__get_payment_endpoint,
                    params={"id_schedule": id_schedule}
                )
                response.raise_for_status()
                return response.json()

        try:
            return await self.__retry_with_backoff(_make_request)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise Exception(
                    "Serviço de pagamentos temporariamente indisponível devido ao alto volume de requisições. "
                    "Por favor, tente novamente em alguns instantes."
                )
            raise Exception(f"Erro ao buscar pagamento: {e.response.status_code} - {e.response.text}")
        except httpx.HTTPError as e:
            raise Exception(f"Erro ao comunicar com o microserviço de pagamentos: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao buscar pagamento: {str(e)}")