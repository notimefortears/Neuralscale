import asyncio
import os

from app.kafka import Producer
from app.generator import generate_event, serialize_event
from app.logging import setup_logging
from app.wait_for_kafka import wait_for_kafka


logger = setup_logging("ingestion")


async def loop() -> None:
    interval_ms = int(os.getenv("INGEST_INTERVAL_MS", "50"))
    producer = Producer()

    logger.info("Waiting for Kafka...")
    await wait_for_kafka(timeout_sec=90)
    logger.info("Kafka reachable. Starting producer...")

    await producer.start()
    logger.info("Producer started. Streaming events...")

    try:
        while True:
            e = generate_event()
            await producer.send_json(serialize_event(e))
            await asyncio.sleep(interval_ms / 1000.0)
    finally:
        logger.info("Stopping producer...")
        await producer.stop()
        logger.info("Producer stopped.")


if __name__ == "__main__":
    asyncio.run(loop())
