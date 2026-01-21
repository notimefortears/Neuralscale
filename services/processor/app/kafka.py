import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

def json_loads(b: bytes) -> dict:
    return json.loads(b.decode("utf-8"))

def json_dumps(d: dict) -> bytes:
    return json.dumps(d, default=str).encode("utf-8")

class KafkaIO:
    def __init__(self, bootstrap: str):
        self.bootstrap = bootstrap
        self.consumer: AIOKafkaConsumer | None = None
        self.producer: AIOKafkaProducer | None = None

    async def start(self, topic_in: str, group_id: str):
        self.consumer = AIOKafkaConsumer(
            topic_in,
            bootstrap_servers=self.bootstrap,
            group_id=group_id,
            value_deserializer=json_loads,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap,
            value_serializer=lambda v: json_dumps(v),
        )
        await self.consumer.start()
        await self.producer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
        if self.producer:
            await self.producer.stop()
