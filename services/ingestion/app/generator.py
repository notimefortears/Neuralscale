import json
import os
import random
import time
import uuid


ACTORS = [
    "APT29", "APT28", "Lazarus", "FIN7", "ScatteredSpider", "UnknownBotnet",
]
TACTICS = [
    "credential_access", "lateral_movement", "persistence", "exfiltration",
    "initial_access", "command_and_control",
]


def _rand_ip() -> str:
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_event() -> dict:
    now = time.time()
    return {
        "event_id": str(uuid.uuid4()),
        "ts": now,
        "actor": random.choice(ACTORS),
        "ip": _rand_ip(),
        "tactic": random.choice(TACTICS),
        "amount": round(random.uniform(1, 5000), 2),
        "merchant": random.choice(["aws", "gcp", "azure", "stripe", "shopify", "unknown"]),
        "user_id": f"user_{random.randint(1, 5000)}",
        "device_id": f"dev_{random.randint(1, 20000)}",
        "country": random.choice(["US", "DE", "AT", "GB", "FR", "NL", "PL", "RO", "IN", "BR"]),
        "channel": random.choice(["web", "mobile", "api"]),
        "label": 1 if random.random() < float(os.getenv("FRAUD_RATE", "0.05")) else 0,
    }


def serialize_event(e: dict) -> bytes:
    return json.dumps(e).encode("utf-8")
