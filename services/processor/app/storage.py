import json
import psycopg

class PostgresStore:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def upsert_event(self, e: dict):
        q = """
        INSERT INTO threat_events (id, source, created_at, title, text, url, severity, entities)
        VALUES (%(id)s, %(source)s, %(created_at)s, %(title)s, %(text)s, %(url)s, %(severity)s, %(entities)s::jsonb)
        ON CONFLICT (id) DO UPDATE SET
          source=EXCLUDED.source,
          created_at=EXCLUDED.created_at,
          title=EXCLUDED.title,
          text=EXCLUDED.text,
          url=EXCLUDED.url,
          severity=EXCLUDED.severity,
          entities=EXCLUDED.entities;
        """
        payload = dict(e)
        payload["entities"] = json.dumps(payload.get("entities", []))
        with psycopg.connect(self.dsn) as conn:
            conn.execute(q, payload)
            conn.commit()
