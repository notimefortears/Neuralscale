import asyncio
import json
import os

from app.consumer import Consumer
from app.graph import GraphWriter
from app.logging import setup_logging
from app.scoring import risk_score
from app.wait_for_kafka import wait_for_kafka


logger = setup_logging("processor")


def _neo4j_cfg() -> tuple[str, str, str]:
    uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "neuralscale")
    return uri, user, password


async def run() -> None:
    logger.info("Waiting for Kafka...")
    await wait_for_kafka(timeout_sec=90)
    logger.info("Kafka reachable. Starting consumer...")

    consumer = Consumer()
    await consumer.start()

    uri, user, pw = _neo4j_cfg()
    graph = GraphWriter(uri=uri, user=user, password=pw)
    graph.ensure_constraints()

    logger.info("Processor started. Consuming events and writing to Neo4j...")

    try:
        async for msg in consumer.get():
            try:
                event = json.loads(msg.value.decode("utf-8"))
            except Exception as e:
                logger.error(f"Bad JSON: {e}")
                continue

            event["score"] = risk_score(event)
            try:
                graph.upsert_event(event)
            except Exception as e:
                logger.error(f"Neo4j write failed: {e}")
    finally:
        logger.info("Shutting down...")
        graph.close()
        await consumer.stop()
        logger.info("Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(run())
