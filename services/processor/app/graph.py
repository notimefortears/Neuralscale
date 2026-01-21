import os
from dataclasses import dataclass
from neo4j import GraphDatabase


@dataclass(frozen=True)
class GraphWriter:
    uri: str
    user: str
    password: str

    def __post_init__(self):
        object.__setattr__(
            self,
            "_driver",
            GraphDatabase.driver(self.uri, auth=(self.user, self.password)),
        )

    def close(self) -> None:
        self._driver.close()

    def ensure_constraints(self) -> None:
        """
        Create constraints/indexes if they don't exist (Neo4j 5+).
        Safe to run on startup.
        """
        statements = [
            "CREATE CONSTRAINT threat_event_id IF NOT EXISTS FOR (e:ThreatEvent) REQUIRE e.event_id IS UNIQUE",
            "CREATE CONSTRAINT actor_name IF NOT EXISTS FOR (a:Actor) REQUIRE a.name IS UNIQUE",
            "CREATE CONSTRAINT ip_value IF NOT EXISTS FOR (i:IPAddress) REQUIRE i.value IS UNIQUE",
            "CREATE INDEX tactic_idx IF NOT EXISTS FOR (e:ThreatEvent) ON (e.tactic)",
        ]
        with self._driver.session() as session:
            for s in statements:
                session.run(s)

    def upsert_event(self, event: dict) -> None:
        q = """
        MERGE (e:ThreatEvent {event_id: $event_id})
        SET e.ts = $ts,
            e.type = $type,
            e.msg = $msg,
            e.score = $score,
            e.tactic = $tactic,
            e.amount = $amount,
            e.merchant = $merchant,
            e.user_id = $user_id,
            e.device_id = $device_id,
            e.country = $country,
            e.channel = $channel,
            e.label = $label

        MERGE (a:Actor {name: $actor})
        MERGE (i:IPAddress {value: $ip})

        MERGE (a)-[:GENERATED]->(e)
        MERGE (e)-[:TARGETED]->(i)
        """
        params = {
            "event_id": event.get("event_id") or event.get("id"),
            "ts": event.get("ts"),
            "type": event.get("type") or event.get("source"),
            "msg": event.get("msg") or event.get("text") or event.get("title"),
            "actor": event.get("actor", "unknown"),
            "ip": event.get("ip", "0.0.0.0"),
            "tactic": event.get("tactic", "unknown"),
            "score": float(event.get("score", 0.0)),
            "amount": float(event.get("amount", 0.0)),
            "merchant": event.get("merchant", "unknown"),
            "user_id": event.get("user_id", "unknown"),
            "device_id": event.get("device_id", "unknown"),
            "country": event.get("country", "unknown"),
            "channel": event.get("channel", "unknown"),
            "label": int(event.get("label", 0)),
        }
        with self._driver.session() as session:
            session.run(q, **params)
