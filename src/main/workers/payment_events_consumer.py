# src/workers/payment_events_consumer.py
import os
import json
import asyncio
import pika

from src.main.composers.client_composers.process_payment_event_composer import process_payment_event_composer

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

class PaymentEventsConsumer:
    def __init__(self, amqp_url: str, exchange: str = "payments"):
        self.__amqp_url = amqp_url
        self.__exchange = exchange
        self.__connection = None
        self.__channel = None
        self.__queue_name = None

    def connect(self):
        params = pika.URLParameters(self.__amqp_url)
        self.__connection = pika.BlockingConnection(params)
        self.__channel = self.__connection.channel()

        self.__channel.exchange_declare(
            exchange=self.__exchange,
            exchange_type="fanout",
            durable=True,
        )

        result = self.__channel.queue_declare(queue="", exclusive=True)
        self.__queue_name = result.method.queue
        self.__channel.queue_bind(exchange=self.__exchange, queue=self.__queue_name)

    async def _handle_message(self, body: bytes):
        data = json.loads(body)
        await process_payment_event_composer(data)

    def _on_message(self, ch, method, properties, body):
        try:
            asyncio.run(self._handle_message(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def start(self):
        if not self.__connection or self.__connection.is_closed:
            self.connect()

        print(f"[*] Waiting for payment events in '{self.__queue_name}'")

        self.__channel.basic_consume(
            queue=self.__queue_name,
            on_message_callback=self._on_message,
        )

        try:
            self.__channel.start_consuming()
        except KeyboardInterrupt:
            self.__channel.stop_consuming()
        finally:
            self.close()

    def close(self):
        if self.__connection and not self.__connection.is_closed:
            self.__connection.close()

def main():
    consumer = PaymentEventsConsumer(RABBITMQ_URL)
    consumer.start()

if __name__ == "__main__":
    main()
