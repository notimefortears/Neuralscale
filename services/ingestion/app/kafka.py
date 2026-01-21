import os
from aiokafka import AIOKafkaProducer


class Producer:
    def __init__(self) -> None:
        self.bootstrap = os.getenv("KAFKA_BOOTSTRAP", "redpanda:9092")
        self.topic = os.getenv("KAFKA_TOPIC_RAW", "neuralscale.raw")
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap,
            acks="all",
            linger_ms=10,
            enable_idempotence=True,
            max_in_flight_requests_per_connection=5,
        )
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()

    async def send_json(self, payload: bytes) -> None:
        if self._producer is None:
            raise RuntimeError("Producer not started")
        await self._producer.send_and_wait(self.topic, payload)
