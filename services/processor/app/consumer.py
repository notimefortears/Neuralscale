import os
from aiokafka import AIOKafkaConsumer


class Consumer:
    def __init__(self) -> None:
        self.bootstrap = os.getenv("KAFKA_BOOTSTRAP", "redpanda:9092")
        self.topic = os.getenv("KAFKA_TOPIC_RAW", "neuralscale.raw")
        self.group = os.getenv("KAFKA_GROUP", "neuralscale-processor")
        self._consumer: AIOKafkaConsumer | None = None

    async def start(self) -> None:
        self._consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap,
            group_id=self.group,
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )
        await self._consumer.start()

    async def stop(self) -> None:
        if self._consumer is not None:
            await self._consumer.stop()

    def get(self) -> AIOKafkaConsumer:
        if self._consumer is None:
            raise RuntimeError("Consumer not started")
        return self._consumer
