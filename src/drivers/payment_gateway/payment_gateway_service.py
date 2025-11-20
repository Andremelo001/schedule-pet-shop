from .interfaces.interface_payment_gateway import InterfacePaymentGateway
from typing import Dict
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

class PaymentGatewayService(InterfacePaymentGateway):
    def __init__(self):
        self.__base_url = os.getenv("MICROSERVICE_URL")
        self.__payment_endpoint = f"{self.__base_url}/payments/generate_payment"
        self.__get_payment_endpoint = f"{self.__base_url}/payments/finder_payment"

    async def generate_payment(self, payment_info: Dict) -> Dict:

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.__payment_endpoint,
                    json=payment_info,
                    timeout=30.0
                )

                response.raise_for_status()

                return response.json()
            
        except httpx.HTTPError as e:
            raise Exception(f"Erro ao comunicar com o microserviço de pagamentos: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Erro inesperado ao processar pagamento: {str(e)}")
        
    async def get_payment(self, id_schedule: str) -> Dict:

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.__get_payment_endpoint,
                    params={"id_schedule": id_schedule}
                )

                response.raise_for_status()

                return response.json()
            
        except httpx.HTTPError as e:
            raise Exception(f"Erro ao comunicar com o microserviço de pagamentos: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Erro inesperado ao processar pagamento: {str(e)}")
