import asyncio
import os
import socket
import time


BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "redpanda:9092")


def _host_port():
    host, port = BOOTSTRAP.split(":")
    return host, int(port)


async def wait_for_kafka(timeout_sec: int = 60) -> None:
    """
    Wait until we can open a TCP connection to the Kafka broker.
    This prevents ingestion from crashing during Redpanda startup.
    """
    host, port = _host_port()
    deadline = time.time() + timeout_sec

    while True:
        try:
            with socket.create_connection((host, port), timeout=1.5):
                return
        except OSError:
            if time.time() > deadline:
                raise RuntimeError(f"Kafka not reachable at {BOOTSTRAP} after {timeout_sec}s")
            await asyncio.sleep(0.5)
