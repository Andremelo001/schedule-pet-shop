from .interfaces.interface_payment_gateway import InterfacePaymentGateway
from typing import Dict
import httpx


class PaymentGatewayService(InterfacePaymentGateway):
    def __init__(self, base_url: str = "http://microservice_payments:8000"):
        self.__base_url = base_url
        self.__payment_endpoint = f"{self.__base_url}/payments/generate_payment"

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
